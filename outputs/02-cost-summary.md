# Cost Estimate — Duplex Apartment

**Model:** `building/Duplex.ifc` · **Prices:** `data/unit-prices.csv` · **Generated:** 2026-06-11

> Quantities are **derived from the 3D geometry** — this model carries no quantity sets. Volumes come from the geometry engine; per-material volumes split a layered element by its layer thicknesses; m² items use face/footprint area. Treat as an **order-of-magnitude design estimate**, not a tender BoQ.

## Cost by trade group

| Trade group | Cost (€) |
|---|---:|
| Structure | 17,587 |
| Envelope | 18,585 |
| Openings | 36,095 |
| Finishes | 30,758 |
| **Grand total** | **103,026** |

_Floor area (sum of room areas, excl. roof): **276 m²** → indicative **€373/m²**_

## Materials in the model with no price (added to nothing — flag for next time)

| Material | Elements affected | Likely price-list gap |
|---|---:|---|
| Metal - Stud Layer | 67 | steel-stud framing (per m² partition) |
| Misc. Air Layers - Air Space | 16 | n/a — air cavity, no cost |
| Masonry - Grout | 6 | grout (per m³ or per m² of block) |
| Wood - Sheathing - plywood | 2 | plywood/OSB sheathing (per m²) |
| Wood - Dimensional Lumber | 2 | softwood framing timber (per m³) |

## Skipped elements (no material or no usable geometry)

| IFC type | Reason | Count |
|---|---|---:|
| IfcFooting | no material assigned | 7 |
| IfcMember | no material assigned | 4 |
| IfcRailing | no material assigned | 4 |
| IfcStair | no material assigned | 2 |
| IfcStairFlight | no material assigned | 2 |
| IfcSlab | no material assigned | 1 |
| IfcRoof | no usable geometry/volume | 1 |

_21 elements skipped — see quality report; mostly the unmateralled footings/members/stairs._

## Method notes & assumptions

- **Material names** are matched to the price book by exact name, then by keyword (so authoring-tool variants like *Type-X Plasterboard* still map to gypsum board); anything unmatched is listed above, not silently zeroed.
- **Layered walls** are costed by their material layers — the plasterboard faces are priced (per m²) even when a steel-stud cavity is the thickest layer, so partitions aren't undercounted.
- **Generic wood flooring** is mapped to **engineered oak (hardwood, €72/m²)** — the model doesn't state hardwood vs. softwood. Softwood (€45/m²) or laminate (€28/m²) would lower the Finishes total.
- **Doors**: 4 hosted in external walls priced as security exterior doors (€1,450); 10 as interior wood (€260).
- **Windows**: 24 priced as uPVC double-glazed (€420/m²) on glazing area (`OverallWidth × OverallHeight`); wide assemblies inflate area.
- **Steel members**: mass = geometry volume × 7,850 kg/m³.
- Reinforcement, MEP, screeds and paint are **not modelled**, so €0 here — a real estimate carries allowances.
