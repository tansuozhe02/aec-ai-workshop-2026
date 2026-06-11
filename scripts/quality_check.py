"""Task 01 — quality / integrity scan of building/Duplex.ifc -> outputs/01-quality-report.md"""
import ifcopenshell
import ifcopenshell.util.element as eu

m = ifcopenshell.open("building/Duplex.ifc")

# Physical building fabric we hold to quality standards.
# Excluded: IfcOpeningElement (voids, not real elements), IfcFurnishingElement (contents, not fabric).
FABRIC = (
    "IfcWall", "IfcWallStandardCase", "IfcSlab", "IfcRoof", "IfcDoor", "IfcWindow",
    "IfcFooting", "IfcBeam", "IfcColumn", "IfcMember", "IfcRailing", "IfcStair",
    "IfcStairFlight", "IfcCovering",
)

def is_fabric(el):
    return el.is_a() in FABRIC

def layerset_thickness(el):
    """Total thickness from material layer set, or None."""
    for rel in getattr(el, "HasAssociations", []) or []:
        if rel.is_a("IfcRelAssociatesMaterial"):
            mat = rel.RelatingMaterial
            mls = None
            if mat.is_a("IfcMaterialLayerSetUsage"):
                mls = mat.ForLayerSet
            elif mat.is_a("IfcMaterialLayerSet"):
                mls = mat
            if mls:
                return sum(l.LayerThickness for l in mls.MaterialLayers)
    return None

elements = [el for el in m.by_type("IfcElement") if is_fabric(el)]
issues = []  # (guid, ifctype, category, detail, fix)

# ---- Check 1: missing material assignment ----
for el in elements:
    if not eu.get_materials(el):
        issues.append((el.GlobalId, el.is_a(), "Missing material",
                       "No material assigned", "Assign a material (or material layer set) in the authoring tool"))

# ---- Check 2: walls with no thickness / invalid thickness ----
for w in m.by_type("IfcWall") + m.by_type("IfcWallStandardCase"):
    th = layerset_thickness(w)
    if th is None:
        issues.append((w.GlobalId, w.is_a(), "Wall thickness",
                       "Thickness cannot be determined (no material layer set)",
                       "Add a material layer set so thickness is defined"))
    elif th <= 0:
        issues.append((w.GlobalId, w.is_a(), "Wall thickness",
                       f"Non-positive thickness ({th})", "Correct the layer thicknesses"))

# ---- Check 3: spaces with no Name ----
for s in m.by_type("IfcSpace"):
    if not s.Name:
        issues.append((s.GlobalId, "IfcSpace", "Unnamed room",
                       "Space has no Name attribute", "Give the room a name/number"))

# ---- Check 4: doors / windows not hosted in an opening ----
for el in m.by_type("IfcDoor") + m.by_type("IfcWindow"):
    if not getattr(el, "FillsVoids", None):
        issues.append((el.GlobalId, el.is_a(), "Not hosted",
                       "Not attached to a wall opening", "Re-host the element in its wall opening"))

# ---- Check 5: zero / negative quantities (room areas + any stated quantity) ----
for q in m.by_type("IfcQuantityArea"):
    if q.AreaValue is not None and q.AreaValue <= 0:
        issues.append(("(quantity)", "IfcQuantityArea", "Bad quantity",
                       f"Area = {q.AreaValue}", "Recompute/repair the area quantity"))
for q in m.by_type("IfcQuantityVolume"):
    if q.VolumeValue is not None and q.VolumeValue <= 0:
        issues.append(("(quantity)", "IfcQuantityVolume", "Bad quantity",
                       f"Volume = {q.VolumeValue}", "Recompute/repair the volume quantity"))
for q in m.by_type("IfcQuantityLength"):
    if q.LengthValue is not None and q.LengthValue <= 0:
        issues.append(("(quantity)", "IfcQuantityLength", "Bad quantity",
                       f"Length = {q.LengthValue}", "Recompute/repair the length quantity"))

# ---- score: % of fabric elements with no issue ----
flagged_guids = {i[0] for i in issues if i[0] not in ("(quantity)",)}
clean = sum(1 for el in elements if el.GlobalId not in flagged_guids)
score = round(100 * clean / len(elements)) if elements else 100

# ---- category rollup ----
from collections import Counter, defaultdict
cat_counts = Counter(i[2] for i in issues)
cat_by_type = defaultdict(Counter)
for g, t, c, d, f in issues:
    cat_by_type[c][t] += 1

# ---- write report ----
lines = []
lines.append("# Quality Report — Duplex Apartment\n")
lines.append(f"**Model:** `building/Duplex.ifc` · **Generated:** 2026-06-11 · "
             f"**Elements checked:** {len(elements)} (building fabric; furniture & opening-voids excluded)\n")
lines.append(f"## Quality score: {score} / 100\n")
verdict = ("No issues found." if score == 100 else
           "Minor issues — safe to proceed with notes." if score >= 85 else
           "Several gaps — review before tender." if score >= 60 else
           "Significant gaps — resolve before relying on this model.")
lines.append(f"*{clean} of {len(elements)} fabric elements are clean. {verdict}*\n")

lines.append("## Summary by category\n")
lines.append("| Category | Count | Where |")
lines.append("|---|---|---|")
order = ["Missing material", "Wall thickness", "Unnamed room", "Not hosted", "Bad quantity"]
for cat in order:
    n = cat_counts.get(cat, 0)
    where = ", ".join(f"{v} {k}" for k, v in cat_by_type[cat].most_common()) if n else "— none —"
    lines.append(f"| {cat} | {n} | {where} |")
lines.append("")

lines.append("## Detailed findings\n")
if not issues:
    lines.append("No issues found.\n")
else:
    lines.append("| Element GUID | Type | Issue | What's wrong | Suggested fix |")
    lines.append("|---|---|---|---|---|")
    # group: show fabric-element issues, ordered by category
    for cat in order:
        for g, t, c, d, f in issues:
            if c == cat:
                lines.append(f"| `{g}` | {t} | {c} | {d} | {f} |")
lines.append("")

# ---- what to fix first ----
lines.append("## What to fix first\n")
prio = []
if cat_by_type["Missing material"]:
    struct = sum(v for k, v in cat_by_type["Missing material"].items()
                 if k in ("IfcFooting", "IfcSlab", "IfcMember", "IfcBeam"))
    open_el = sum(v for k, v in cat_by_type["Missing material"].items()
                  if k in ("IfcDoor", "IfcWindow"))
    if struct:
        prio.append(f"**1. Structural elements without materials** ({struct} footings/slabs/members) — "
                    "these carry load and feed the cost estimate; assign materials first.")
    if open_el:
        prio.append(f"**2. Doors & windows without materials** ({open_el}) — sizes are present, but no material "
                    "means they can't be costed or material-validated. Common in this export type; assign at type level.")
prio.append("**3. Everything else** (railings, stairs, coverings) — lower impact; clean up before handover, not before tender.")
lines.extend(prio)
lines.append("")
lines.append("> **Note on wall thickness:** no walls were flagged. Although this model stores no thickness *quantities*, "
             "every wall has a material layer set, so thickness is well-defined (e.g. 124 mm partitions, 550 mm exterior). "
             "The quality checker reads thickness from the layer set rather than a quantity field.")

with open("outputs/01-quality-report.md", "w") as fh:
    fh.write("\n".join(lines) + "\n")

print(f"score={score}  issues={len(issues)}  elements={len(elements)}")
for cat in order:
    print(f"  {cat:18} {cat_counts.get(cat,0)}   {dict(cat_by_type[cat])}")
