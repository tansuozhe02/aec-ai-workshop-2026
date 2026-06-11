# Task 1 — Quality Check

Read the IFC model at `building/Duplex.ifc` and produce a quality report.

## Check for

- Elements missing a material assignment
- Walls with no thickness or invalid quantity
- Spaces with no `Name` attribute
- Doors or windows not attached to an opening
- Anything with zero or negative quantity

## Output

Write a Markdown report at `outputs/01-quality-report.md` with:

- A quality score at the top (0–100), where 100 means no issues found
- A summary line per category (e.g. "3 walls missing thickness")
- A detailed table: element GUID, IFC type, what's wrong, suggested fix
- A short paragraph at the bottom: "what to fix first" — prioritized

## Suggested approach

`ifcopenshell` is the standard Python library for reading IFC files. Install it if it's not already present:

```bash
pip install ifcopenshell
```

You don't need to be perfect on the first pass — get something readable, then we'll iterate.
