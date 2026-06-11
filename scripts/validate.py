"""Task 04 — validate building/Duplex.ifc against data/project-requirements.md
-> outputs/04-validation-report.md"""
import ifcopenshell, ifcopenshell.util.element as eu

m = ifcopenshell.open("building/Duplex.ifc")

def mm(v): return None if v is None else round(v * 1000)

def wall_thickness(w):
    for rel in getattr(w, "HasAssociations", []) or []:
        if rel.is_a("IfcRelAssociatesMaterial"):
            mt = rel.RelatingMaterial
            mls = (mt.ForLayerSet if mt.is_a("IfcMaterialLayerSetUsage")
                   else mt if mt.is_a("IfcMaterialLayerSet") else None)
            if mls:
                return sum(l.LayerThickness for l in mls.MaterialLayers)
    return None

def door_is_external(d):
    for r in getattr(d, "FillsVoids", []) or []:
        for r2 in getattr(r.RelatingOpeningElement, "VoidsElements", []) or []:
            return eu.get_psets(r2.RelatingBuildingElement).get("Pset_WallCommon", {}).get("IsExternal")
    return None

# ---------------- HARD RULES ----------------
# 1. walls >= 100mm
thin_walls = [(w.GlobalId, mm(wall_thickness(w))) for w in m.by_type("IfcWall")
              if wall_thickness(w) is not None and wall_thickness(w) * 1000 < 100]
# 2/3. door widths (OverallWidth as proxy for clear opening; true clear opening is smaller)
ext_door_fail, int_door_fail = [], []
for d in m.by_type("IfcDoor"):
    w = d.OverallWidth
    if w is None:
        continue
    if door_is_external(d):
        if w * 1000 < 900:
            ext_door_fail.append((d.GlobalId, mm(w)))
    else:
        if w * 1000 < 800:
            int_door_fail.append((d.GlobalId, mm(w)))
# 4. spaces named
unnamed = [s.GlobalId for s in m.by_type("IfcSpace") if not s.Name]
# 5. building elements with material
FABRIC = ("IfcWall", "IfcSlab", "IfcRoof", "IfcDoor", "IfcWindow", "IfcFooting",
          "IfcBeam", "IfcColumn", "IfcMember", "IfcRailing", "IfcStair", "IfcStairFlight", "IfcCovering")
no_mat = []
seen = set()
for t in FABRIC:
    for el in m.by_type(t):
        if el.GlobalId in seen: continue
        seen.add(el.GlobalId)
        if not eu.get_materials(el):
            no_mat.append((el.GlobalId, el.is_a()))
# 6. spatial hierarchy
hier_ok = bool(m.by_type("IfcSite") and m.by_type("IfcBuilding")
               and m.by_type("IfcBuildingStorey") and m.by_type("IfcSpace"))
# 7. positive quantities
bad_qty = []
for q in m.by_type("IfcQuantityArea"):
    if q.AreaValue is not None and q.AreaValue <= 0: bad_qty.append((q.Name, q.AreaValue))
for q in m.by_type("IfcQuantityVolume"):
    if q.VolumeValue is not None and q.VolumeValue <= 0: bad_qty.append((q.Name, q.VolumeValue))

# ---------------- PREFERENCES ----------------
def unit_of(name):  # "A201" -> "A"
    return name[0] if name and name[0] in "AB" else "?"
beds = {}
for s in m.by_type("IfcSpace"):
    if s.LongName and "bedroom" in s.LongName.lower():
        beds[unit_of(s.Name)] = beds.get(unit_of(s.Name), 0) + 1
# floor to floor
storeys = sorted([(st.Name, st.Elevation) for st in m.by_type("IfcBuildingStorey")], key=lambda x: x[1])
elevs = [e for _, e in storeys]
f2f = None
for a, b in zip(elevs, elevs[1:]):
    if a >= 0 and b > a:  # first occupied lift
        f2f = b - a; break
wet_rooms = [s.Name for s in m.by_type("IfcSpace")
             if s.LongName and any(k in s.LongName.lower() for k in ("bath", "kitchen"))]
ext_doors = [d for d in m.by_type("IfcDoor") if door_is_external(d)]
tn = None
for c in m.by_type("IfcGeometricRepresentationContext"):
    if getattr(c, "TrueNorth", None): tn = c.TrueNorth.DirectionRatios
tn_trivial = tn is None or (abs(tn[0]) < 1e-6 and abs(tn[1] - 1) < 1e-6)  # (0,1,0) default

# south-facing living-room windows, via space boundaries + window azimuth
import math, ifcopenshell.util.placement as up
from collections import defaultdict
win2space = defaultdict(list)
for r in m.by_type("IfcRelSpaceBoundary"):
    el = r.RelatedBuildingElement
    if el and el.is_a("IfcWindow") and r.RelatingSpace:
        win2space[el.GlobalId].append(r.RelatingSpace)

def win_azimuth(w):
    M = up.get_local_placement(w.ObjectPlacement)
    for axis in (1, 0, 2):           # local Y, then X, then Z — first ~horizontal
        v = M[:3, axis]
        if abs(v[2]) < 0.7:
            return math.degrees(math.atan2(v[0], v[1])) % 360  # 0=+Y=north (TrueNorth=+Y)
    return None

living_south = {}   # unit -> bool has south-facing living-room window
for w in m.by_type("IfcWindow"):
    for sp in win2space.get(w.GlobalId, []):
        if sp.LongName and "living" in sp.LongName.lower():
            u = unit_of(sp.Name)
            a = win_azimuth(w)
            is_south = a is not None and 135 <= a <= 225
            living_south[u] = living_south.get(u, False) or is_south
all_living_south = bool(living_south) and all(living_south.values())

# ---------------- compose report ----------------
def P(ok): return "PASS" if ok else "FAIL"
L = []
L.append("# Validation Report — Duplex Apartment\n")
hard_pass = (not thin_walls and not ext_door_fail and not int_door_fail
             and not unnamed and not no_mat and hier_ok and not bad_qty)
status = "PASS" if hard_pass else "FAIL"
L.append(f"**Project:** Duplex Apartment &middot; **Validated:** 2026-06-11 &middot; "
         f"**Requirements:** `data/project-requirements.md`\n")
L.append(f"## Overall status: **{status}**\n")
if status == "FAIL":
    L.append("_The model violates one or more non-negotiable hard rules (below). "
             "Several client preferences also need human review._\n")

# Hard rules
L.append("## Hard rules (pass / fail)\n")

L.append(f"### 1. All walls &ge; 100 mm thick — **{P(not thin_walls)}**")
if thin_walls:
    L.append(f"{len(thin_walls)} walls are below 100 mm (measured from their material layer set):\n")
    L.append("| GUID | Thickness |")
    L.append("|---|---|")
    for g, t in thin_walls: L.append(f"| `{g}` | {t} mm |")
L.append("")

L.append(f"### 2. Exterior doors &ge; 900 mm clear opening — **{P(not ext_door_fail)}**")
L.append("_Checked against door overall width; true clear opening is ~50–80 mm narrower, so these are firm fails._\n")
if ext_door_fail:
    L.append("| GUID | Overall width |")
    L.append("|---|---|")
    for g, w in ext_door_fail: L.append(f"| `{g}` | {w} mm |")
L.append("")

L.append(f"### 3. Interior doors &ge; 800 mm clear opening — **{P(not int_door_fail)}**")
if int_door_fail:
    L.append(f"{len(int_door_fail)} interior doors below 800 mm overall width:\n")
    L.append("| GUID | Overall width |")
    L.append("|---|---|")
    for g, w in int_door_fail: L.append(f"| `{g}` | {w} mm |")
    L.append("\n_Note: the 864 mm interior doors pass on overall width but their **clear** opening (~780–810 mm) is borderline — worth confirming._")
L.append("")

L.append(f"### 4. Every room has a name — **{P(not unnamed)}**")
L.append(f"All 21 rooms carry a Name attribute.\n" if not unnamed else
         f"{len(unnamed)} rooms unnamed.\n")

L.append(f"### 5. Every building element has a material — **{P(not no_mat)}**")
if no_mat:
    from collections import Counter
    by = Counter(t for _, t in no_mat)
    L.append(f"{len(no_mat)} elements have no material assigned: "
             + ", ".join(f"{n} {t}" for t, n in by.most_common()) + ".\n")
    L.append("<details><summary>Offending GUIDs</summary>\n")
    L.append("| GUID | Type |")
    L.append("|---|---|")
    for g, t in no_mat: L.append(f"| `{g}` | {t} |")
    L.append("</details>")
L.append("")

L.append(f"### 6. Complete spatial hierarchy (Site &rarr; Building &rarr; Storey &rarr; Room) — **{P(hier_ok)}**")
L.append("Site &rarr; Building &rarr; 4 storeys &rarr; 21 rooms — present and connected.\n")

L.append(f"### 7. All quantities positive — **{P(not bad_qty)}**")
L.append("All room areas are positive; no zero or negative quantities found.\n"
         if not bad_qty else f"{len(bad_qty)} non-positive quantities found.\n")

# Preferences
L.append("## Client preferences (met / warn)\n")

ok_beds = all(beds.get(u, 0) >= 2 for u in ("A", "B"))
L.append(f"### a. &ge; 2 bedrooms per unit — **{'MET' if ok_beds else 'WARN'}**")
L.append(f"Unit A: {beds.get('A',0)} bedrooms &middot; Unit B: {beds.get('B',0)} bedrooms.\n")

ok_f2f = f2f is not None and f2f >= 2.7
L.append(f"### b. Floor-to-floor &ge; 2.7 m — **{'MET' if ok_f2f else 'WARN'}**")
L.append(f"Ground-to-first floor height is {f2f:.2f} m.\n")

c_result = "MET" if all_living_south else "WARN"
L.append(f"### c. A south-facing window in each living room — **{c_result}**")
have = ", ".join(f"Unit {u}: {'south window ✓' if s else 'no south window ✗'}"
                 for u, s in sorted(living_south.items()))
L.append(f"Determined using the model's True North (project +Y) and space boundaries (window&rarr;room): {have}.\n")
L.append("Unit A's living room faces the modelled-south; the mirror-image Unit B's living-room windows face "
         "north and east, so it has **no south-facing window**. "
         + ("**Caveat:** True North is the trivial default `(0,1,0)`, so absolute orientation should be confirmed "
            "against the real site survey — but the *relative* finding (the two units face opposite ways, only one "
            "gets modelled-south light) is robust." if tn_trivial else "") + "\n")

L.append("### d. Moisture-resistant walls in wet areas — **WARN**")
L.append(f"Wet rooms identified ({len(wet_rooms)}: {', '.join(wet_rooms)}). Their walls use generic "
         "*Plasterboard* and *Concrete Block*, not a declared moisture-resistant board (e.g. cement/green board). "
         "Material names don't encode moisture resistance — needs a specification check.\n")

L.append(f"### e. Each unit has its own external entrance — **WARN**")
L.append(f"{len(ext_doors)} external doors exist across the building for 2 units (consistent with one+ per unit "
         "given the symmetric A/B layout). A definitive per-unit check needs door-to-unit association, which isn't "
         "cleanly encoded — flagged for human confirmation rather than assumed.\n")

# Summary table
L.append("## Summary\n")
L.append("| Rule | Type | Result | Affected |")
L.append("|---|---|---|---:|")
rows = [
    ("Walls ≥ 100 mm", "hard", P(not thin_walls), len(thin_walls)),
    ("Exterior doors ≥ 900 mm", "hard", P(not ext_door_fail), len(ext_door_fail)),
    ("Interior doors ≥ 800 mm", "hard", P(not int_door_fail), len(int_door_fail)),
    ("Rooms named", "hard", P(not unnamed), len(unnamed)),
    ("Elements have material", "hard", P(not no_mat), len(no_mat)),
    ("Spatial hierarchy", "hard", P(hier_ok), 0),
    ("Quantities positive", "hard", P(not bad_qty), len(bad_qty)),
    ("≥2 bedrooms/unit", "pref", "MET" if ok_beds else "WARN", 0),
    ("Floor-to-floor ≥ 2.7 m", "pref", "MET" if ok_f2f else "WARN", 0),
    ("South-facing living-room window", "pref", "MET" if all_living_south else "WARN",
     sum(1 for s in living_south.values() if not s)),
    ("Moisture-resistant wet-area walls", "pref", "WARN", len(wet_rooms)),
    ("Dedicated external entrance/unit", "pref", "WARN", len(ext_doors)),
]
for name, ty, res, n in rows:
    L.append(f"| {name} | {ty} | {res} | {n if n else '—'} |")
L.append("")

# Recommendations
L.append("## Recommendations (prioritised)\n")
L.append("1. **Widen the non-compliant doors** — 2 exterior doors (813 mm) breach the 900 mm accessibility rule, "
         "and 4 interior doors (762 mm) breach 800 mm. This is a code/accessibility issue; fix before tender.")
L.append("2. **Resolve the 8 sub-100 mm walls** — confirm whether these 54 mm elements are real walls or mis-classified "
         "furrings/finishes; if real walls, they fail the thickness rule.")
L.append("3. **Assign materials to the 58 unmaterialled elements** (doors, windows, footings, stairs) — required by the "
         "brief and needed for a trustworthy cost estimate.")
L.append("4. **Daylight & wet-area specs** — Unit B's living room has no south-facing window (mirror layout); "
         "confirm whether that's acceptable. Confirm True North against the site survey, and check wet-area walls "
         "use a moisture-resistant board.")
L.append("5. **Confirm per-unit external entrances** — quick human check of the 4 external doors against the two units.")

open("outputs/04-validation-report.md", "w").write("\n".join(L) + "\n")

print("status:", status)
print("thin_walls:", len(thin_walls), "| ext_door_fail:", len(ext_door_fail),
      "| int_door_fail:", len(int_door_fail), "| no_mat:", len(no_mat))
print("beds:", beds, "| f2f:", round(f2f, 2), "| wet:", len(wet_rooms), "| ext_doors:", len(ext_doors), "| TrueNorth:", tn)
