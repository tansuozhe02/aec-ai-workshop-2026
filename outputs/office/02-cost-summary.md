# Cost Estimate — Project Number

**Model:** `building/Office_A.ifc` · **Prices:** `data/unit-prices.csv` · **Generated:** 2026-06-11

> Quantities are **derived from the 3D geometry** — this model carries no quantity sets. Volumes come from the geometry engine; per-material volumes split a layered element by its layer thicknesses; m² items use face/footprint area. Treat as an **order-of-magnitude design estimate**, not a tender BoQ.

## Cost by trade group

| Trade group | Cost (€) |
|---|---:|
| Envelope | 39,273 |
| Openings | 85,950 |
| Finishes | 94,124 |
| **Grand total** | **219,347** |

_Floor area (sum of room areas, excl. roof): **3,582 m²** → indicative **€61/m²**_

## Materials in the model with no price (added to nothing — flag for next time)

| Material | Elements affected | Likely price-list gap |
|---|---:|---|
| Metal - Stud Layer | 476 | steel-stud framing (per m² partition) |
| Default | 81 | add to price list |
| Ceiling Tile 600 x 600 | 81 | add to price list |
| Wood - Sheathing - plywood | 18 | plywood/OSB sheathing (per m²) |
| Misc. Air Layers - Air Space | 16 | n/a — air cavity, no cost |
| Laminate - Ivory, Matte | 13 | add to price list |
| Metal - Firring | 2 | add to price list |

## Skipped elements (no material or no usable geometry)

| IFC type | Reason | Count |
|---|---|---:|
| IfcRailing | no material assigned | 10 |
| IfcMember | no material assigned | 8 |
| IfcStairFlight | no material assigned | 4 |
| IfcSlab | no material assigned | 2 |
| IfcStair | no material assigned | 2 |

_26 elements skipped — see quality report; mostly the unmateralled footings/members/stairs._

## Method notes & assumptions

- **Material names** are matched to the price book by exact name, then by keyword (so authoring-tool variants like *Type-X Plasterboard* still map to gypsum board); anything unmatched is listed above, not silently zeroed.
- **Layered walls** are costed by their material layers — the plasterboard faces are priced (per m²) even when a steel-stud cavity is the thickest layer, so partitions aren't undercounted.
- **Doors**: 6 hosted in external walls priced as security exterior doors (€1,450); 96 as interior wood (€260).
- **Windows**: 69 priced as uPVC double-glazed (€420/m²) on glazing area (`OverallWidth × OverallHeight`); wide assemblies inflate area.
- Reinforcement, MEP, screeds and paint are **not modelled**, so €0 here — a real estimate carries allowances.
