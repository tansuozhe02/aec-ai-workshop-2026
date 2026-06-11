# What we need from this model

We received `building/Duplex.ifc` from the architect (a 2-unit residential duplex, design-development stage). Below are the things the firm needs from it.

Each one is a **short brief — the ask, not a step-by-step spec.** Pick one and hand it to Claude (*"do task 2 from TASKS.md"*). The professional *how* for every task lives once in **`docs/ifc-workflows.md`** — that's the firm's playbook, and Claude applies it. Reports land in `outputs/`.

---

### 0. Get to know the model
Before anyone commits budget or programme, the PM wants to know: **what is this, what's in it, and can we trust it?** Produce the plain-language intake memo — what's the project, what's in the model, what's missing or weak, and what it's actually good enough for.
→ `outputs/00-model-overview.md`

### 1. Check the model quality
We're about to lean on this model for costing and compliance. First, **what's broken or missing in the data?** Produce a quality report: a headline score, what's wrong by category, the offending elements, and a prioritised "fix this first" list.
→ `outputs/01-quality-report.md`

### 2. Estimate the cost
The client wants a **ballpark material cost** before we go to tender. Our price book is `data/unit-prices.csv`. Produce a per-element breakdown plus a summary rolled up by trade — with an honest basis: what's included, what isn't, and anything we couldn't price.
→ `outputs/02-cost-breakdown.csv` + `outputs/02-cost-summary.md`

### 3. Summarise it for the client
The client is a property developer — they read numbers, not IFC schemas. Pull together the quality check and the cost estimate into a **one-page summary** they can skim and decide from: project at a glance, what it costs and where the money is, how much we trust the model, and the few things they really need to know.
→ `outputs/03-client-report.html` (one printable page, DataDrivenAEC purple `#7c3aed`, self-contained)

### 4. Validate against the brief
We also have the client's design brief in `data/project-requirements.md`. Before tender, confirm **whether the model meets it.** The brief mixes hard, non-negotiable rules with softer preferences — separate the two: what passes, what fails (with the offending elements), what needs a human to check. Where the model can't prove something, say so — don't fake a pass.
→ `outputs/04-validation-report.md`

---

When you're happy with a result, ask Claude to **save it as a skill** so you can re-run it on the next project with one command. That's the point — not five scripts, but five pieces of the firm's expertise, bottled.
