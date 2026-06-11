# AEC AI Workshop — Live Demo

A 20-minute build along: use Claude Code to turn an IFC model into a quality report, a cost estimate, and a client-facing summary — and save each step as a reusable skill.

## What's in here

```
building/Duplex.ifc              — buildingSMART standard duplex (2.3 MB)
data/unit-prices.csv             — sample €/unit material prices
data/project-requirements.md     — client brief (hard rules + preferences)
tasks/00-explore.md              — PM-friendly model overview (start here)
tasks/01-quality-check.md        — quality / integrity scan
tasks/02-cost-estimate.md        — cost rollup using unit prices
tasks/03-client-report.md        — 1-page client summary (HTML)
tasks/04-validation.md           — validation against project requirements
.claude/skills/                  — empty; we fill this live
outputs/                         — Claude writes here
```

## How to follow along

1. Click **Code → Codespaces → Create codespace on main**
2. Wait ~60 seconds for the environment to boot
3. In the terminal: `npm install -g @anthropic-ai/claude-code && claude`
4. Authenticate with your Anthropic console account
5. Ask Claude: *"Read `tasks/01-quality-check.md` and do what it says."*

When you're happy with the result, ask Claude to **save it as a skill**:

> "Save what we just did as a skill called `model-quality-check` so I can run it again with `/model-quality-check`."

Then try task 2. Then task 3. Watch `.claude/skills/` fill up.

## What you actually built

Not three scripts. Three pieces of your firm's expertise, bottled, reusable, shareable.

— @DataDrivenAEC
