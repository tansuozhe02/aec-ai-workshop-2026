# Task 4 — Model Validation

Validate the IFC model at `building/Duplex.ifc` against the project requirements in `data/project-requirements.md`.

The requirements file mixes two kinds of rules:

1. **Hard rules** — pass/fail compliance (dimensions, attributes, materials)
2. **Client preferences** — softer expectations that should produce a warning if missing or unclear

You'll need to read the requirements in plain English and apply them to the IFC.

## Output

Write `outputs/04-validation-report.md` with:

- **Header**: project name, validation date, overall status (PASS / PASS WITH WARNINGS / FAIL)
- **Hard rules section**: for each rule → PASS or FAIL → if FAIL, list the offending element GUIDs and why
- **Client preferences section**: for each preference → MET or WARN → if WARN, explain what's missing or unclear
- **Summary table**: rule, type (hard / preference), result, count of affected elements
- **Recommendations**: a short prioritized list of what to fix before tender

## Notes

- Some preferences may be impossible to verify from geometry alone (e.g., "south-facing window") — explain what you'd need to check those properly. Don't fake a PASS.
- If a rule is ambiguous, surface it rather than guess.
- Re-use `ifcopenshell` from earlier tasks.
