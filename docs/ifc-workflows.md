# How professionals work an IFC model — methodology for each task

*The `tasks/` briefs say **what** to produce. This document says **how a professional actually approaches it** — the standard method, the conventions, the pitfalls, and what "good" looks like. Each task's skill should carry this method, so every run applies the firm's expertise, not just a script.*

Grounded in real findings from `building/Duplex.ifc` (buildingSMART sample, Revit 2011, IFC2X3 Coordination View).

---

## A first principle: trust nothing until you've audited the model

An IFC is a **claim about a building**, exported by some tool, at some level of detail, for some purpose. Before any task, a professional asks:

- **What view definition / purpose was it exported for?** A *Coordination View* (like the Duplex) is for clash/coordination — it often ships **without quantities**. A *Quantity Takeoff View* carries them. The export purpose tells you what's missing before you look.
- **What's the Level of Development (LOD)?** Geometry present ≠ information present. A wall can look perfect and carry no material, no thickness, no fire rating.
- **Garbage in, garbage out.** Every downstream number inherits the model's gaps. Surface them first, in writing.

> **Duplex reality:** the model has full geometry and a complete spatial tree, but **no volume/length quantities at all** and a placeholder project name (`"0001"`). Both facts change how every later task must be done — so they belong in the *first* report, not discovered halfway through costing.

---

## Task 00 — Model intake / exploration

**What a professional does on receiving the model:** opens it once, end to end, and writes the "can I trust this?" memo a PM needs *before* committing budget or programme to it. Not a schema dump — a fitness assessment.

**Standard method**
1. Read the header for **provenance** — authoring tool, date, author, schema, view definition.
2. Walk the **spatial hierarchy** (Project → Site → Building → Storey → Space) and confirm it's complete and connected.
3. Take a **census** — count every element type; sum floor areas per storey; count rooms and units.
4. List **materials** and where they're used; flag anything non-standard.
5. Run the **smell test** — what's missing, weak, or placeholder.

**Conventions & standards:** gross vs. net floor area (state which); IFC spatial containment rules; recognised material naming.

**Common pitfalls:** areas stored in non-standard property sets (the Duplex hides them in a `GSA Space Areas` set, not `BaseQuantities`); placeholder metadata; a storey with zero rooms that's actually structural (the Duplex `T/FDN` foundation level).

**What "good" looks like:** a one-page memo a non-technical PM understands, ending in a **"ready for X?" matrix** (cost / validation / client summary / handover) with ✓/⚠/✗ and a one-line why for each.

---

## Task 01 — Quality / integrity check

**What a professional does:** runs a model-checking pass (the manual equivalent of Solibri / IDS rules) to catch the data defects that will bite downstream — *before* they corrupt a cost plan or a compliance report.

**Standard method**
1. **Completeness** — every element has a material; every room has a name/number; quantities present or derivable.
2. **Validity** — no zero/negative quantities; dimensions within sane ranges.
3. **Relational integrity** — doors/windows hosted in openings; elements contained in a storey.
4. **Score and prioritise** — a headline metric plus a "fix this first" list ranked by downstream impact.

**Conventions & standards:** buildingSMART **IDS** (Information Delivery Specification) is the emerging standard for "what must be present"; **BCF** is how you'd issue the findings back to the design team.

**Common pitfalls / judgement calls:**
- **Don't false-flag on absence of one representation.** The Duplex stores no thickness *quantity*, but every wall has a **material layer set** — thickness is well-defined (124 mm / 550 mm). A naive "no thickness quantity" check flags all 57 walls and tanks the score. Read thickness from the layer set instead, and **document the reasoning**.
- Decide scope explicitly — is furniture in or out? (We excluded `IfcFurnishingElement` and opening voids; we said so.)

**What "good" looks like:** a transparent score, a per-category summary, a GUID-level table an modeller can act on, and a note on every judgement call (so the score is defensible, not magic).

---

## Task 02 — Cost estimate

**What a professional (a quantity surveyor / cost engineer) does:** this is **not** "quantity × rate." It's a structured estimate with a stated basis, exclusions, and a confidence level.

**Standard method**
1. **Measurability audit** — is the model fit to measure? If quantities are absent, decide your source: **derive from geometry** or fall back to manual takeoff.
2. **Quantity takeoff (QTO)** — extract per element. For the Duplex, this means the **geometry engine** computes volumes; layered elements are split by layer-thickness fraction.
3. **Classify** — roll quantities into a cost structure: trade groups here (Structure / Envelope / Openings / Finishes / MEP); in practice **RICS NRM**, **Uniclass**, or **MasterFormat/UniFormat**.
4. **Apply unit rates** — from a price book or historical project data; localise to region and date.
5. **Add what the model doesn't carry** — labour, preliminaries, overheads & profit, contingency, and **un-modelled scope**: reinforcement, MEP, screeds, paint, groundworks.
6. **Sanity-check** — benchmark **€/m²** against comparable projects. If it's an order of magnitude off, the takeoff is wrong, not the building.
7. **State the basis of estimate** — assumptions, exclusions, confidence, what would change the number most.

**Conventions & standards:** RICS NRM1 (order-of-cost) / NRM2 (detailed measurement); gross internal area (GIA) for €/m²; rates exclusive vs. inclusive of labour.

**Common pitfalls:**
- **The "primary material" trap.** Costing each element by its single thickest layer breaks on stud partitions — the thickest layer is the **steel-stud cavity**, which has no bulk price. Cost by **layers** so the plasterboard faces (the real cost) are captured; flag the stud-framing line as missing rather than zeroing it.
- **Silent unit mismatches** — m³ vs m² vs each. A door is a *count*; glazing is *area*; concrete is *volume*. Match the rate's unit, don't assume.
- **Missing materials = €0.** Unpriced ≠ free. The Duplex's 58 unmateralled elements (doors, windows, footings) must be **listed as exclusions**, not silently dropped to zero.

**What "good" looks like:** a per-element breakdown (CSV) **and** a summary with trade totals, a €/m² benchmark, an explicit list of materials not found in the price book, skipped elements with reasons, and a "basis & assumptions" section. Labelled **order-of-magnitude design estimate**, never "the price."

---

## Task 03 — Client-facing summary

**What a professional does:** translates the technical work into the three or four numbers a developer or owner actually decides on — and says nothing in IFC jargon.

**Standard method**
1. Lead with **project facts** (area, units, storeys, structure) and the **headline cost**.
2. Show **where the money is** (cost by trade) — that's where their choices have leverage.
3. Give a **quality/confidence read** in one sentence ("ready for tender" vs "resolve 3 issues first").
4. End with **3 things they should know** — risks and levers in plain English.

**Conventions:** round sensibly (€ to the nearest 100, area to the nearest m²); one printable page; never expose GUIDs or `IfcWall`.

**Common pitfalls:** false precision (don't print €103,026 as if it's a tender price); hiding the caveats the estimate depends on (materials-only, derived quantities); burying the lede under data.

**What "good" looks like:** a one-page, on-brand summary where every number is **traceable to the underlying reports** (so re-running the model updates it), and the "three things" are genuinely decision-relevant.

---

## Task 04 — Validation against requirements

**What a professional does:** checks the model against the client's brief and applicable codes — separating **hard pass/fail compliance** from **softer preferences**, and being honest about what geometry can and can't prove.

**Standard method**
1. **Parse the requirements** into machine-checkable rules; classify each as **hard** (fail = non-compliant) or **preference** (warn).
2. **Check each rule against the model**, citing the offending element GUIDs on failure.
3. For anything **not provable from geometry alone**, say so and state what you'd need — **never fake a PASS**.
4. Produce a **prioritised fix list** ordered by severity and how blocking it is to tender.

**Conventions & standards:** this is where **buildingSMART IDS** shines — requirements as a formal, executable spec. Accessibility dimensions (door clear widths) trace to local building codes / ADA / Part M.

**Common pitfalls & nuances:**
- **Clear opening ≠ overall width.** A door's `OverallWidth` includes the frame; the *clear* opening is ~50–80 mm less. If overall width already fails the rule, the clear opening definitely does — a robust fail. If it passes by a hair, flag it borderline. *(Duplex: 813 mm exterior doors fail the 900 mm rule outright; 864 mm interior doors are borderline on clear opening.)*
- **Orientation needs True North.** "South-facing window" is unprovable without the project's True North **and** a window→room link. *(Duplex: it has both — `TrueNorth=(0,1,0)` plus 265 space boundaries — so we found Unit A's living room faces south and the mirror-image Unit B's does not. But `(0,1,0)` is the trivial default, so the absolute orientation needs confirming against the site survey, even though the relative finding is solid.)* This is the model judgement to get right: extract the real answer where the data supports it, and **scope the caveat precisely** where it doesn't.
- **Material names don't encode performance.** "Moisture-resistant in wet areas" can't be confirmed from a material called "Plasterboard" — that's a specification check, so WARN.

**What "good" looks like:** a header verdict (PASS / PASS-WITH-WARNINGS / FAIL), hard rules with GUID-level evidence, preferences with honest MET/WARN and *what's needed* for the unprovable ones, a summary table, and a prioritised pre-tender fix list.

---

## The thread through all five

Every task starts the same way: **audit the model's fitness for *this* purpose, then do the work the model actually supports — no more, no less, and say what it doesn't support.** That honesty *is* the professional value. A tool that fakes a clean number is worse than useless; a tool that says "here's what I can stand behind, here's what needs a human, and here's why" is the expertise worth bottling into a skill.
