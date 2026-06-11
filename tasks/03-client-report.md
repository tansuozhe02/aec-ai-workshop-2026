# Task 3 — Client Report

Generate a 1-page client-facing summary of the Duplex project.

Audience: a developer or property owner who reads numbers, not IFC schemas.

## Include

- **Project at a glance**: name, gross floor area, number of stories, primary structural material
- **Cost summary**: total + per-trade-group breakdown (read from `outputs/02-cost-breakdown.csv`)
- **Quality status**: the score from `outputs/01-quality-report.md` plus a one-sentence interpretation ("Model is ready for tender" / "Resolve 3 critical issues before issue" / etc.)
- **3 things the client should know**: 3 short bullets. Plain English. Examples: "Envelope is 38% of cost — material substitution here has the biggest leverage" or "5 walls have unspecified thickness — affects insulation calc and final cost"

## Style

- One A4 page when printed
- No IFC jargon (no "IfcWall", no "GUID")
- Numbers rounded sensibly (€ to nearest 100, areas to nearest m²)
- HTML output, purple-themed (`#7c3aed`) to match DataDrivenAEC branding

## Output

Write `outputs/03-client-report.html`. Make it self-contained — inline CSS, no external dependencies.
