# Model Intake Report — Duplex Apartment

*Prepared for the project manager, before any checks are run. Plain-language overview of what the model is, what's in it, and whether it can be trusted for the work ahead.*

**File:** `building/Duplex.ifc` · **Generated:** 2026-06-11

---

## Project at a glance

| | |
|---|---|
| **Project** | "Duplex Apartment" *(see flag — the project's official name field just says "0001")* |
| **Building type** | 2-unit residential duplex |
| **Location** | Latitude 41°52′27″ N, Longitude 87°38′21″ W — *this is Chicago, USA* (site labelled only "Default") |
| **Authoring tool** | Autodesk Revit Architecture 2011 |
| **Model created** | 7 September 2011 |
| **Author / company** | *Blank — not recorded in the file* |
| **File format** | IFC 2x3, "Coordination View" export |
| **Stories** | 4 (Foundation, Level 1, Level 2, Roof) |
| **Rooms** | 21 |
| **Units** | 2 (an "A" unit and a "B" unit — mirror-image layout) |
| **Livable floor area** | **≈ 276 m²** (138 m² per unit, across two floors) |
| **Roof footprint** | 146 m² |

---

## The spatial story — floor by floor

| Floor | Height (level) | Rooms | Floor area | Looks…|
|---|---|---|---|---|
| Roof | +6.00 m | 1 | 146 m² (footprint) | OK — single roof object |
| Level 2 (bedrooms) | +3.10 m | 10 | ≈ 135 m² | Balanced — 5 rooms per unit |
| Level 1 (living) | 0.00 m | 10 | ≈ 142 m² | Balanced — 5 rooms per unit |
| Foundation (T/FDN) | −1.25 m | 0 | — | Expected — structural level, no rooms |

**Floor-to-floor height: 3.10 m** (Level 1 → Level 2) — comfortably above a typical 2.7 m minimum.

Each unit is laid out as you'd expect for a duplex:
- **Level 1:** Foyer, Living Room, Kitchen, a Bathroom, plus a stair/utility room
- **Level 2:** 2 Bedrooms, a second Bathroom, Hallway, Utility

Both units are complete and symmetric — no obviously empty or duplicated floors. This is a healthy-looking model.

---

## What's in it — element census

| Element | Count |
|---|---|
| Walls | 57 |
| Furniture / fixtures | 61 |
| Windows | 24 |
| Slabs (floors/ceilings) | 21 |
| Doors | 14 |
| Coverings (finishes) | 13 |
| Beams | 8 |
| Footings | 7 |
| Structural members | 4 |
| Railings | 4 |
| Stairs (+ 2 flights) | 2 |
| Roof | 1 |
| *Openings (cut-outs for doors/windows)* | *50* |

---

## Materials present

18 distinct materials, **all recognisable, standard construction materials** — nothing exotic or mis-named:

| Material | Used on (≈ elements) |
|---|---|
| Metal stud + Plasterboard | 63 each *(internal partition walls)* |
| Concrete block (masonry) | 16 |
| Air space *(a wall cavity layer, not a real material)* | 16 |
| Rigid insulation | 13 |
| Brick (masonry) | 12 |
| Cast-in-situ concrete | 9 |
| Structural steel (345 MPa) | 8 |
| Wood flooring | 8 |
| Semi-rigid insulation | 8 |
| Ceramic tile | 6 |
| Grout, plywood, lumber, concrete, grass, roofing membranes | 1–6 each |

No unknown materials. The only odd entry is *"Air Space,"* which is a cavity layer inside wall build-ups rather than a purchasable material — normal, but worth knowing it'll show up in any material list.

---

## Smell test — what's missing or weak

These are things a PM would want to raise with the design team. Not graded by severity — just surfaced.

- ⚠️ **The model has almost no measured quantities.** It contains room *areas* (one per room), but **no wall thicknesses, no volumes, no lengths** anywhere. Anything that needs "how much concrete / brick / m³" will have to be **calculated from the 3D geometry**, not simply read off the model.
- ⚠️ **Project name is a placeholder** — the official project field reads `"0001"`. The real name ("Duplex Apartment") is only in a secondary description field.
- ⚠️ **Building name is blank**, and the **site is just labelled "Default."**
- ⚠️ **Author and company are blank** in the file header — no record of who produced it.
- ⚠️ **All 14 doors and all 24 windows have no material assigned** in the standard way. (Their materials live in Revit-specific notes, not in the proper IFC material field.) Door and window *sizes*, however, are present.
- ⚠️ **Other elements with no material:** 7 footings, 4 structural members, 4 railings, 2 stairs, 1 slab, and the 61 furniture items.
- ℹ️ **Room areas are stored in a non-standard place** ("GSA Space Areas"). They're correct, but tools that look only in the usual spot will report "no areas found" — we had to look in the right place.
- ℹ️ **Window count may be misleading** — at least one "window" is a wide assembly (~4.8 m). The count of 24 reflects IFC objects, not necessarily 24 separate openings you'd picture.

**Good news:** the spatial hierarchy is complete and correct (Site → Building → 4 Floors → 21 Rooms), **every room has a name**, and every door/window is properly hosted in a wall opening. The bones of the model are sound.

---

## Can I trust this for…?

| Use case | Ready? | Why / why not |
|---|---|---|
| **Cost estimate** | ⚠ | Room areas are good, but there are **no wall/slab/structure volumes or thicknesses** and doors/windows carry no material. Quantities must be *derived from geometry* before costing — doable, but not a simple read-off. |
| **Validation against client brief** | ⚠ | Door/window **sizes are present** (good for accessibility checks). Wall thickness and "south-facing window" must be **computed from geometry**; materials are mostly present. Most rules checkable, a few need geometric analysis. |
| **Client-facing summary** | ✓ | Plenty here for a high-level summary: area, floors, unit count, materials, a clean layout. Safe to produce now. |
| **Handover / facilities management** | ✗ | Placeholder project name, blank author/building name, missing quantities, and unclassified door/window materials make this **not handover-grade** as-is. |

---

### Bottom line for the PM
This is a **clean, well-structured architectural model** of a two-unit duplex — good enough to summarise for a client today, and a solid base for quality, cost, and compliance work. The **one thing to flag to the design team** is that the model was exported without measured quantities, so any cost or material-volume work will rely on calculating from the geometry rather than reading numbers the modeller put in. The placeholder project/author metadata should also be filled in before this model is handed onward.
