# Task 2 — Cost Estimate

Using the IFC model at `building/Duplex.ifc` and the unit prices in `data/unit-prices.csv`, produce a cost estimate.

## How

1. For each element in the IFC, identify its primary material
2. Look up that material in `data/unit-prices.csv`
3. Multiply the IFC quantity (m², m³, or unit count — depending on the price unit) by the unit price
4. Sum into trade groups: **Structure**, **Envelope**, **Openings**, **Finishes**, **MEP**

## Output

Write two files:

- `outputs/02-cost-breakdown.csv` — one row per element with: GUID, IFC type, material, quantity, unit, unit_price, line_total, trade_group
- `outputs/02-cost-summary.md` — totals per trade group, grand total, and a list of any materials in the model that were **not** found in the price list (so we know what to add next time)

## Edge cases

- If a material isn't in the price list, flag it in the CSV (`unit_price = 0`, `note = "missing from price list"`) but still include the row
- If quantities are missing on an element, skip it but list it in the summary's "skipped elements" section

## Suggested approach

Re-use the IFC reading approach from Task 1. Use `pandas` for the CSV side.
