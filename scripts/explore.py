"""Task 00 — walk the Duplex model once and collect everything for the intake report."""
import ifcopenshell
from ifcopenshell.util import element as eu
from ifcopenshell.util import unit as uu
from collections import Counter, defaultdict
import json

m = ifcopenshell.open("building/Duplex.ifc")

# ---- units ----
length_unit = uu.get_project_unit(m, "LENGTHUNIT")
area_scale = uu.calculate_unit_scale(m) ** 2  # to m^2 (length scale squared)

def get_qty(el, names):
    """Return first matching base quantity value from element's quantity sets."""
    psets = eu.get_psets(el, qtos_only=True)
    for qset in psets.values():
        for k, v in qset.items():
            if k in names and isinstance(v, (int, float)):
                return v
    return None

# ---- spatial: stories ----
stories = []
for st in m.by_type("IfcBuildingStorey"):
    spaces = [r for r in eu.get_decomposition(st) if r.is_a("IfcSpace")]
    area = 0.0
    space_info = []
    for sp in spaces:
        a = get_qty(sp, {"GrossFloorArea", "NetFloorArea", "Area"})
        a = (a or 0.0)
        area += a
        space_info.append((sp.Name, sp.LongName, a, sp.GlobalId))
    stories.append({
        "name": st.Name,
        "elev": st.Elevation,
        "n_spaces": len(spaces),
        "area": area,
        "spaces": space_info,
    })

# ---- element census ----
census = Counter()
for el in m.by_type("IfcElement"):
    census[el.is_a()] += 1

# ---- materials ----
mat_counts = Counter()
no_material = []
for el in m.by_type("IfcElement"):
    mats = eu.get_materials(el)
    if not mats:
        no_material.append((el.is_a(), el.GlobalId))
    seen = set()
    for mat in mats:
        nm = getattr(mat, "Name", None) or "(unnamed)"
        if nm not in seen:
            mat_counts[nm] += 1
            seen.add(nm)

# ---- smell test ----
spaces_no_name = [(s.GlobalId, s.LongName) for s in m.by_type("IfcSpace") if not s.Name]
sites = m.by_type("IfcSite")
proj = m.by_type("IfcProject")[0]

# walls with no thickness qty
walls_no_thick = []
for w in m.by_type("IfcWall"):
    t = get_qty(w, {"Width", "Thickness"})
    if not t:
        walls_no_thick.append(w.GlobalId)

# doors/windows not in an opening (no FillsVoids)
doors_no_opening = [d.GlobalId for d in m.by_type("IfcDoor") if not getattr(d, "FillsVoids", None)]
wins_no_opening = [w.GlobalId for w in m.by_type("IfcWindow") if not getattr(w, "FillsVoids", None)]

out = {
    "schema": m.schema,
    "proj_name": proj.Name,
    "proj_long": getattr(proj, "LongName", None),
    "site": [(s.Name, s.RefLatitude, s.RefLongitude, s.RefElevation) for s in sites],
    "building": [(b.Name, getattr(b, "LongName", None)) for b in m.by_type("IfcBuilding")],
    "length_unit": str(length_unit),
    "n_stories": len(m.by_type("IfcBuildingStorey")),
    "stories": stories,
    "n_spaces": len(m.by_type("IfcSpace")),
    "census": dict(census.most_common()),
    "materials": dict(mat_counts.most_common()),
    "no_material": no_material,
    "spaces_no_name": spaces_no_name,
    "walls_no_thick": walls_no_thick,
    "doors_no_opening": doors_no_opening,
    "wins_no_opening": wins_no_opening,
}
print(json.dumps(out, indent=2, default=str))
