# AEC AI Workshop — Live Demo

A 20-minute build along: use Claude Code to turn an IFC model into a quality report, a cost estimate, and a client-facing summary — and save each step as a reusable skill.

## What's in here

```
building/Duplex.ifc              — buildingSMART standard duplex (2.3 MB)   ← the model we received
data/unit-prices.csv             — our firm's price book (€/unit)
data/project-requirements.md     — the client's design brief (hard rules + preferences)
TASKS.md                         — the five things we need from the model (start here)
docs/ifc-workflows.md            — the firm's playbook: how a pro does each task
.claude/skills/                  — empty; we fill this live
outputs/                         — where the reports land
viewer/                          — optional self-contained 3D viewer for the model
```

`TASKS.md` holds five deliberately **short handoff briefs** — *"we got this file, we need this thing"* — not step-by-step specs. The professional *how* lives once in `docs/ifc-workflows.md`, and Claude applies it. That separation is the point: the brief is the ask, the playbook is the expertise, the skill is the bottled result.

## How to follow along

1. Click **Code → Codespaces → Create codespace on main**
2. Wait ~60 seconds for the environment to boot
3. In the terminal: `npm install -g @anthropic-ai/claude-code && claude`
4. Authenticate with your Anthropic console account
5. Ask Claude: *"Read `TASKS.md` and do task 0."*

When you're happy with the result, ask Claude to **save it as a skill**:

> "Save what we just did as a skill called `model-quality-check` so I can run it again with `/model-quality-check`."

Then try task 2. Then task 3. Watch `.claude/skills/` fill up.

## What you actually built

Not three scripts. Three pieces of your firm's expertise, bottled, reusable, shareable.

— @DataDrivenAEC
