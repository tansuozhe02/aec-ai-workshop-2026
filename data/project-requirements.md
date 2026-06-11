# Duplex Project — Design Requirements

Client: ACME Real Estate
Project: 2-unit residential duplex, suburban site
Phase: Design Development

## Hard rules — model must pass

These are non-negotiable compliance items. The model fails validation if any are violated.

- All walls must have a thickness of at least **100 mm**
- All exterior doors must have a clear opening width of at least **900 mm** (accessibility)
- All interior doors must have a clear opening width of at least **800 mm**
- Every space (`IfcSpace`) must have a `Name` attribute filled in
- Every building element must have at least one material assigned
- The model must contain a complete spatial hierarchy: `IfcSite → IfcBuilding → IfcBuildingStorey → IfcSpace`
- All quantities must be positive (no zero or negative areas, volumes, or counts)

## Client preferences — flag with WARN if not clearly met

These are softer expectations. They may not be fully verifiable from geometry alone — when in doubt, raise a warning rather than guess.

- At least **2 bedrooms per unit**
- Floor-to-floor height of at least **2.7 m**
- Each living room should have at least one window oriented to the south (best practice for daylight in northern hemisphere)
- Wet-area walls (bathrooms, kitchens) should use a moisture-resistant material
- Each unit should have its own dedicated entrance from outside

## Out of scope for this validation

- Energy / thermal performance (separate model)
- Structural calculation (engineer's responsibility)
- Fire-safety compliance (separate review)

## Deliverable

A validation report (Markdown) that an architect can hand to the client showing: what passes, what fails, what needs human review, and a prioritized fix list.
