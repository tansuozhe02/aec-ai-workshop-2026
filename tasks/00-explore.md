# Task 00 — Explore the Model

Open the IFC at `building/Duplex.ifc` and produce the overview a project manager would want on day one — *before* anyone runs a single check on it.

Think of this as the "model intake report." A PM doesn't care about IFC schemas. They care about:

- **What is this?** (project, building, basic facts)
- **What's in it?** (counts, materials, the spatial story)
- **What's missing?** (the smell test — would I trust this for cost / tender / handover?)
- **Who made it, when?** (provenance, version, authoring tool)

## What to include in the report

### Project at a glance
- Project name, building name, site location (if present)
- Authoring tool and date the model was created
- Number of stories
- Gross floor area (sum of `IfcSpace` areas)
- Number of spaces / rooms
- Number of units (if discoverable from space names or groupings)

### Element census
A table of every `IfcElement` type with its count. Walls, doors, windows, slabs, columns, beams, stairs, spaces — whatever's in there.

### Materials present
List of materials used in the model with the count of elements assigned to each. Flag any materials Claude doesn't recognize as standard construction materials.

### Spatial breakdown
For each story: name, elevation, floor area, number of spaces. The PM should be able to tell at a glance whether the model is balanced (e.g., "ground floor 180 m², first floor 200 m²") or suspicious (e.g., "first floor 0 m²").

### Smell test — what's missing or weak
A short bulleted list. Examples:
- "12 spaces have no Name attribute"
- "8 walls have no material assigned"
- "No `IfcSite` found — model has no geographic context"
- "Quantities are missing on 3 elements"

Don't try to grade severity — just surface what a PM would want to flag for the design team.

### The "can I trust this for…" matrix
A short table answering:

| Use case | Ready? | Why / why not |
|---|---|---|
| Cost estimate | ✓ / ⚠ / ✗ | … |
| Validation against client brief | ✓ / ⚠ / ✗ | … |
| Client-facing summary | ✓ / ⚠ / ✗ | … |
| Handover / FM | ✓ / ⚠ / ✗ | … |

## Output

Write `outputs/00-model-overview.md`. Plain language, no IFC jargon in headings (the PM doesn't know what `IfcSpace` is — call them "rooms").

## Suggested approach

`pip install ifcopenshell` if needed. Walk the model once, collect everything, then format the report.
