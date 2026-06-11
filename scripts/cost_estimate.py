"""Task 02 — cost estimate for building/Duplex.ifc.

Model has no quantity sets, so quantities are derived from geometry:
  - m3 materials  -> layer volume (element volume split by layer-thickness fraction)
  - m2 materials  -> face area (wall elevation, or slab/covering footprint)
  - kg materials  -> layer volume x density
  - unit          -> count (doors)
  - windows       -> glazing area (OverallWidth x OverallHeight)

Outputs:
  outputs/02-cost-breakdown.csv
  outputs/02-cost-summary.md
"""
import csv
import ifcopenshell
import ifcopenshell.geom as geom
import ifcopenshell.util.element as eu
import ifcopenshell.util.shape as ushape
import pandas as pd

STEEL_DENSITY = 7850  # kg/m3

m = ifcopenshell.open("building/Duplex.ifc")
prices = pd.read_csv("data/unit-prices.csv")
PRICE = {r.material: r for r in prices.itertuples(index=False)}

# model material name -> price-list key  (None = deliberately unmapped)
MAT_MAP = {
    "Concrete - Cast In Situ": "concrete_c30",
    "Concrete": "concrete_c30",
    "Masonry - Concrete Block": "masonry_block",
    "Masonry - Brick": "masonry_brick",
    "Insulation / Thermal Barriers - Rigid insulation": "xps_insulation",
    "Insulation / Thermal Barriers - Semi-rigid insulation": "mineral_wool",
    "Plasterboard": "gypsum_board",
    "Metal - Steel - 345 MPa": "structural_steel",
    "Wood - Flooring": "hardwood_floor",   # assumption: engineered oak; see summary
    "Ceramic Tile": "ceramic_tile",
}
# materials present in the model but with no price-list equivalent
UNMAPPED_KNOWN = {
    "Masonry - Grout", "Metal - Stud Layer", "Wood - Sheathing - plywood",
    "Wood - Dimensional Lumber", "Misc. Air Layers - Air Space",
    "Site - Grass", "Roofing - Barrier", "Roofing - EPDM Membrane",
}

settings = geom.settings()

def geom_metrics(el):
    """Return (volume, footprint_area, side_area) in m / m2 / m3, or None on failure."""
    try:
        shp = geom.create_shape(settings, el)
    except Exception:
        return None
    g = shp.geometry
    vol = ushape.get_volume(g)
    verts = ushape.get_vertices(g)
    mn, mx = ushape.get_bbox(verts)
    dx, dy, dz = (mx - mn)
    footprint = float(dx * dy)
    horiz = sorted([float(dx), float(dy)])
    side_area = horiz[1] * float(dz)   # length x height
    return float(vol), footprint, side_area

def layers(el):
    """List of (material_name, thickness) for a layered element, else None."""
    for rel in getattr(el, "HasAssociations", []) or []:
        if rel.is_a("IfcRelAssociatesMaterial"):
            mat = rel.RelatingMaterial
            mls = (mat.ForLayerSet if mat.is_a("IfcMaterialLayerSetUsage")
                   else mat if mat.is_a("IfcMaterialLayerSet") else None)
            if mls:
                return [(l.Material.Name if l.Material else None, l.LayerThickness)
                        for l in mls.MaterialLayers]
    return None

def single_material(el):
    ms = eu.get_materials(el)
    return ms[0].Name if ms else None

def host_wall_is_external(door):
    for r in getattr(door, "FillsVoids", []) or []:
        op = r.RelatingOpeningElement
        for r2 in getattr(op, "VoidsElements", []) or []:
            w = r2.RelatingBuildingElement
            return eu.get_psets(w).get("Pset_WallCommon", {}).get("IsExternal")
    return None

rows = []          # breakdown rows
skipped = []       # (guid, type, reason)
unmapped_seen = {} # material -> count of elements

def price_row(key):
    return PRICE.get(key)

def add_line(el, material_name, qty, unit, price_key):
    pr = price_row(price_key) if price_key else None
    if pr is None:
        unmapped_seen[material_name] = unmapped_seen.get(material_name, 0) + 1
        rows.append([el.GlobalId, el.is_a(), material_name, round(qty, 4), unit or "",
                     0.0, 0.0, "(unpriced)", "missing from price list"])
        return
    line_total = qty * pr.unit_price_eur
    rows.append([el.GlobalId, el.is_a(), material_name, round(qty, 4), pr.unit,
                 pr.unit_price_eur, round(line_total, 2), pr.trade_group, ""])

WALL_LIKE = ("IfcWall", "IfcWallStandardCase")
SLAB_LIKE = ("IfcSlab", "IfcRoof", "IfcCovering", "IfcFooting", "IfcStair", "IfcStairFlight")

def cost_layered_element(el, gm):
    vol, footprint, side_area = gm
    ls = layers(el)
    area_basis = side_area if el.is_a() in WALL_LIKE else footprint
    if not ls:
        return False
    total_t = sum(t for _, t in ls if t) or 1.0
    for name, t in ls:
        if not name:
            continue
        key = MAT_MAP.get(name)
        pr = price_row(key) if key else None
        if pr is None:
            add_line(el, name, vol * (t / total_t), "m3", None)  # unpriced, qty informational
            continue
        if pr.unit == "m3":
            add_line(el, name, vol * (t / total_t), "m3", key)
        elif pr.unit == "m2":
            add_line(el, name, area_basis, "m2", key)
        elif pr.unit == "kg":
            add_line(el, name, vol * (t / total_t) * STEEL_DENSITY, "kg", key)
    return True

def cost_single_material(el, gm, name):
    vol, footprint, side_area = gm
    key = MAT_MAP.get(name)
    pr = price_row(key) if key else None
    if pr is None:
        add_line(el, name, vol, "m3", None)
        return
    if pr.unit == "m3":
        add_line(el, name, vol, "m3", key)
    elif pr.unit == "m2":
        add_line(el, name, footprint if el.is_a() in SLAB_LIKE else side_area, "m2", key)
    elif pr.unit == "kg":
        add_line(el, name, vol * STEEL_DENSITY, "kg", key)

# ---- doors ----
for d in m.by_type("IfcDoor"):
    ext = host_wall_is_external(d)
    key = "door_exterior_security" if ext else "door_interior_wood"
    add_line(d, "(exterior door)" if ext else "(interior door)", 1, "unit", key)

# ---- windows ----
for w in m.by_type("IfcWindow"):
    ow, oh = w.OverallWidth, w.OverallHeight
    if not ow or not oh:
        skipped.append((w.GlobalId, "IfcWindow", "missing OverallWidth/Height"))
        continue
    add_line(w, "(glazing)", float(ow) * float(oh), "m2", "window_double_glazed")

# ---- fabric (walls, slabs, roof, footings, beams, members, coverings, stairs, railings) ----
FABRIC = ("IfcWall", "IfcSlab", "IfcRoof", "IfcFooting", "IfcBeam",
          "IfcMember", "IfcCovering", "IfcStair", "IfcStairFlight", "IfcRailing")
done = set()
for t in FABRIC:
    for el in m.by_type(t):
        if el.GlobalId in done:
            continue
        done.add(el.GlobalId)
        ls = layers(el)
        sm = single_material(el)
        if not ls and not sm:
            skipped.append((el.GlobalId, el.is_a(), "no material assigned"))
            continue
        gm = geom_metrics(el)
        if gm is None or gm[0] <= 0:
            skipped.append((el.GlobalId, el.is_a(), "no usable geometry/volume"))
            continue
        if ls:
            cost_layered_element(el, gm)
        else:
            cost_single_material(el, gm, sm)

# ---- write breakdown CSV ----
with open("outputs/02-cost-breakdown.csv", "w", newline="") as fh:
    wtr = csv.writer(fh)
    wtr.writerow(["GUID", "ifc_type", "material", "quantity", "unit",
                  "unit_price", "line_total", "trade_group", "note"])
    wtr.writerows(rows)

# ---- roll up ----
from collections import defaultdict
trade_tot = defaultdict(float)
for r in rows:
    if r[7] not in ("(unpriced)",):
        trade_tot[r[7]] += r[6]
grand = sum(trade_tot.values())

TRADE_ORDER = ["Structure", "Envelope", "Openings", "Finishes", "MEP"]
lines = []
lines.append("# Cost Estimate — Duplex Apartment\n")
lines.append("**Model:** `building/Duplex.ifc` · **Prices:** `data/unit-prices.csv` · **Generated:** 2026-06-11\n")
lines.append("> Quantities are **derived from the 3D geometry** — this model carries no quantity sets. "
             "Volumes come from the geometry engine; per-material volumes split a layered element by its layer "
             "thicknesses; m² items use face/footprint area. Treat as an **order-of-magnitude design estimate**, not a tender BoQ.\n")
lines.append("## Cost by trade group\n")
lines.append("| Trade group | Cost (€) |")
lines.append("|---|---:|")
for tr in TRADE_ORDER:
    if tr in trade_tot:
        lines.append(f"| {tr} | {trade_tot[tr]:,.0f} |")
lines.append(f"| **Grand total** | **{grand:,.0f}** |")
lines.append("")
lines.append(f"_Indicative cost per m² of livable area (≈276 m²): **€{grand/276:,.0f}/m²**_\n")

lines.append("## Materials in the model with no price (added to nothing — flag for next time)\n")
if unmapped_seen:
    lines.append("| Material | Elements affected | Likely price-list gap |")
    lines.append("|---|---:|---|")
    hint = {
        "Metal - Stud Layer": "steel-stud framing (per m² partition)",
        "Masonry - Grout": "grout (per m³ or per m² of block)",
        "Wood - Sheathing - plywood": "plywood/OSB sheathing (per m²)",
        "Wood - Dimensional Lumber": "softwood framing timber (per m³)",
        "Misc. Air Layers - Air Space": "n/a — air cavity, no cost",
        "Site - Grass": "n/a — landscaping, out of building scope",
        "Roofing - Barrier": "roofing underlay / vapour barrier (per m²)",
        "Roofing - EPDM Membrane": "EPDM membrane (per m²)",
    }
    for mat, n in sorted(unmapped_seen.items(), key=lambda kv: -kv[1]):
        lines.append(f"| {mat} | {n} | {hint.get(mat, 'add to price list')} |")
lines.append("")

lines.append("## Skipped elements (no material or no usable geometry)\n")
if skipped:
    from collections import Counter
    sc = Counter((t, reason) for _, t, reason in skipped)
    lines.append("| IFC type | Reason | Count |")
    lines.append("|---|---|---:|")
    for (t, reason), n in sc.most_common():
        lines.append(f"| {t} | {reason} | {n} |")
    lines.append(f"\n_{len(skipped)} elements skipped — see quality report; mostly the unmateralled footings/members/stairs._")
lines.append("")

lines.append("## Method notes & assumptions\n")
lines.append("- **Stud partition walls** cost only their plasterboard faces (per m²); the steel-stud cavity has no price line, so it is flagged above, not silently zeroed.")
lines.append("- **\"Wood - Flooring\"** mapped to **engineered oak (hardwood, €72/m²)** — the model doesn't say hardwood vs. softwood. Swapping to softwood (€45/m²) or laminate (€28/m²) would lower the Finishes total.")
lines.append("- **Doors**: 4 hosted in external walls priced as security exterior doors (€1,450); 10 as interior wood (€260).")
lines.append("- **Windows**: priced as uPVC double-glazed (€420/m²) on glazing area; the model includes some wide assemblies, so window area is on the high side.")
lines.append("- **Steel beams**: mass = geometry volume × 7,850 kg/m³.")
lines.append("- Reinforcement steel, MEP, and finishes paint/screed are **not modelled**, so €0 here — a real estimate would carry allowances.")

with open("outputs/02-cost-summary.md", "w") as fh:
    fh.write("\n".join(lines) + "\n")

# ---- console ----
print(f"rows={len(rows)}  skipped={len(skipped)}  grand=EUR {grand:,.0f}")
for tr in TRADE_ORDER:
    if tr in trade_tot:
        print(f"  {tr:10} {trade_tot[tr]:12,.0f}")
print("unmapped materials:", dict(unmapped_seen))
