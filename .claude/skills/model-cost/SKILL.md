---
name: model-cost
description: Produce a material cost estimate from an IFC/BIM model using a unit-price book. Use when the user wants a cost estimate, cost breakdown, quantity takeoff, or "how much will this building cost" from a .ifc file. Rolls costs up by trade group (Structure / Envelope / Openings / Finishes / MEP), derives quantities from geometry when the model carries none, and reports an honest basis with exclusions.
---

# Model cost estimate

Generates an order-of-magnitude **material** cost estimate from an IFC model and a unit-price CSV. Built for design-stage models that may not carry quantity sets — it derives volumes and areas from the geometry when needed.

## How to run

The skill bundles a ready quantity-takeoff script. From the repo root:

```bash
python3 .claude/skills/model-cost/cost_estimate.py \
  --model building/Duplex.ifc \
  --prices data/unit-prices.csv \
  --outdir outputs
```

All three flags default to those paths, so a bare `python3 .claude/skills/model-cost/cost_estimate.py` works for this project. Point `--model`/`--prices` elsewhere to run it on any other IFC + price book.

It writes two files to `--outdir`:
- `02-cost-breakdown.csv` — one row per element-material: GUID, type, material, quantity, unit, unit price, line total, trade group, note
- `02-cost-summary.md` — totals by trade, grand total, €/m², unpriced materials, skipped elements, and the basis/assumptions

After running, read the summary and give the user the trade totals, the grand total, the biggest cost driver, and the headline caveats.

## The method it applies (so you can defend or adapt the numbers)

This is **not** "quantity × rate." A professional estimate has a stated basis:

1. **Measurability audit first.** If the model has no quantity sets (common for a Coordination-View export), don't fail — **derive quantities from the geometry**. The script uses ifcopenshell's geometry engine for volumes and bounding boxes; layered elements are split by layer-thickness fraction.
2. **Match the rate's unit.** m³ → volume, m² → face/footprint area, kg → volume × density (steel 7850 kg/m³), unit → count. Never assume.
3. **Cost by layers, not a single "primary" material.** A stud partition's thickest layer is the steel-stud cavity, which has no bulk price — costing by primary material would zero it. Cost the plasterboard faces (the real driver) and **flag the missing stud line** rather than hiding it.
4. **Unpriced ≠ free.** List every model material with no price-book match as an explicit exclusion (unit_price 0, noted), not a silent zero.
5. **Classify into trade groups** taken from the price book's `trade_group` column (Structure / Envelope / Openings / Finishes / MEP).
6. **Sanity-check** with a €/m² benchmark. If it's an order of magnitude off, the takeoff is wrong, not the building.
7. **State the basis.** Label it an order-of-magnitude *design* estimate, not a tender bill of quantities. Materials only — no labour, preliminaries, contingency, reinforcement, or MEP unless modelled.

Full background: `docs/ifc-workflows.md` §2.

## Watch out for

- **Doors**: priced per unit; classify exterior vs interior by the host wall's `IsExternal` and use the right rate.
- **Windows**: priced on glazing area (`OverallWidth × OverallHeight`); wide assemblies inflate area — note it.
- **Material name mismatch**: the model's authoring-tool names (e.g. `Masonry - Concrete Block`) won't match price-book keys (`masonry_block`); the script carries a mapping — extend it for a new price book.
