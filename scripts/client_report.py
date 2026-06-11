"""Task 03 — one-page client HTML summary -> outputs/03-client-report.html
Reads cost from outputs/02-cost-breakdown.csv and quality score from outputs/01-quality-report.md."""
import re
import pandas as pd

# ---- cost (from task 02) ----
df = pd.read_csv("outputs/02-cost-breakdown.csv")
priced = df[df.line_total > 0]
trade = priced.groupby("trade_group").line_total.sum()
TRADES = ["Structure", "Envelope", "Openings", "Finishes", "MEP"]
trade = {t: float(trade.get(t, 0.0)) for t in TRADES if trade.get(t, 0.0) > 0}
grand = sum(trade.values())

def r100(x):
    return int(round(x / 100.0) * 100)

# ---- quality score (from task 01) ----
qtext = open("outputs/01-quality-report.md").read()
score = int(re.search(r"Quality score:\s*(\d+)", qtext).group(1))
missing_mat = int(re.search(r"Missing material \|\s*(\d+)", qtext).group(1))

# ---- project facts ----
GFA = 276
STORIES = 2          # occupied floors (plus foundation + roof)
UNITS = 2
PROJECT = "Duplex Apartment"
STRUCT_MAT = "Reinforced concrete & masonry block"

if score >= 85:
    q_word, q_class, q_msg = "Good", "ok", "Model is essentially tender-ready."
elif score >= 60:
    q_word, q_class, q_msg = "Fair", "warn", "Usable for design, but resolve the material gaps before going to tender."
else:
    q_word, q_class, q_msg = "Poor", "bad", "Significant gaps — clean up the model before relying on it."

open_pct = round(100 * trade.get("Openings", 0) / grand)
fin_pct = round(100 * trade.get("Finishes", 0) / grand)

# three things the client should know
bullets = [
    f"<b>Windows &amp; doors are the single biggest cost ({open_pct}% of the total).</b> "
    "That's where material choices have the most leverage — and the model includes a few oversized window "
    "assemblies worth confirming before they drive the glazing budget.",

    "<b>This is a materials-only estimate, read from the 3D model's geometry.</b> "
    "It excludes labour, mechanical/electrical/plumbing, and reinforcement, which the model doesn't yet carry. "
    "Use it to compare options and spot cost drivers — expect the all-in build figure to be materially higher.",

    f"<b>{missing_mat} elements (most doors, windows and some structure) have no material specified yet.</b> "
    f"That's why the quality score is {score}/100. None are structural defects — but assigning those materials "
    "would tighten the estimate and is worth doing before tender.",
]

bars = "".join(
    f'<div class="bar"><span class="lab">{t}</span>'
    f'<span class="track"><i style="width:{round(100*v/max(trade.values()))}%"></i></span>'
    f'<span class="val">&euro;{r100(v):,}</span></div>'
    for t, v in sorted(trade.items(), key=lambda kv: -kv[1])
)

html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{PROJECT} — Client Summary</title>
<style>
  :root {{ --p:#7c3aed; --p2:#a78bfa; --ink:#1e1b2e; --mut:#6b7280; --line:#ece9f5; }}
  * {{ box-sizing:border-box; }}
  body {{ font:15px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
         color:var(--ink); margin:0; background:#f5f3fb; }}
  .page {{ max-width:820px; margin:24px auto; background:#fff; padding:40px 48px;
           box-shadow:0 2px 20px rgba(124,58,237,.10); border-radius:12px; }}
  header {{ border-bottom:3px solid var(--p); padding-bottom:16px; margin-bottom:24px;
            display:flex; justify-content:space-between; align-items:flex-end; }}
  h1 {{ font-size:26px; margin:0; color:var(--p); }}
  .sub {{ color:var(--mut); font-size:13px; }}
  .brand {{ font-weight:700; color:var(--p); letter-spacing:.5px; }}
  h2 {{ font-size:13px; text-transform:uppercase; letter-spacing:.8px; color:var(--p);
        margin:28px 0 12px; }}
  .grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; }}
  .stat {{ background:#faf8ff; border:1px solid var(--line); border-radius:10px; padding:14px; }}
  .stat .n {{ font-size:22px; font-weight:700; color:var(--ink); }}
  .stat .k {{ font-size:12px; color:var(--mut); }}
  .total {{ display:flex; align-items:baseline; gap:12px; margin:6px 0 14px; }}
  .total .big {{ font-size:38px; font-weight:800; color:var(--p); }}
  .total .unit {{ color:var(--mut); }}
  .bar {{ display:grid; grid-template-columns:90px 1fr 90px; align-items:center; gap:10px; margin:7px 0; }}
  .bar .lab {{ font-size:13px; }}
  .bar .track {{ background:#efeafe; border-radius:6px; height:14px; overflow:hidden; }}
  .bar .track i {{ display:block; height:100%; background:linear-gradient(90deg,var(--p),var(--p2)); }}
  .bar .val {{ text-align:right; font-variant-numeric:tabular-nums; font-size:13px; color:var(--mut); }}
  .quality {{ display:flex; align-items:center; gap:16px; background:#faf8ff;
              border:1px solid var(--line); border-radius:10px; padding:16px; }}
  .score {{ width:64px; height:64px; border-radius:50%; display:flex; align-items:center; justify-content:center;
            font-size:22px; font-weight:800; color:#fff; flex:none; }}
  .ok {{ background:#16a34a; }} .warn {{ background:#d97706; }} .bad {{ background:#dc2626; }}
  .quality .word {{ font-weight:700; }}
  ol {{ padding-left:20px; }} ol li {{ margin:10px 0; }}
  footer {{ margin-top:28px; padding-top:14px; border-top:1px solid var(--line);
            color:var(--mut); font-size:11px; display:flex; justify-content:space-between; }}
  @media print {{ body{{background:#fff;}} .page{{box-shadow:none; margin:0; max-width:none;}} }}
</style></head>
<body><div class="page">
  <header>
    <div><h1>{PROJECT}</h1><div class="sub">Client summary &middot; prepared 11 June 2026</div></div>
    <div class="brand">DataDrivenAEC</div>
  </header>

  <h2>Project at a glance</h2>
  <div class="grid">
    <div class="stat"><div class="n">{GFA} m&sup2;</div><div class="k">Livable floor area</div></div>
    <div class="stat"><div class="n">{UNITS} units</div><div class="k">Residential duplex</div></div>
    <div class="stat"><div class="n">{STORIES} floors</div><div class="k">Plus foundation &amp; roof</div></div>
    <div class="stat"><div class="n">RC + block</div><div class="k">Primary structure</div></div>
  </div>

  <h2>Estimated material cost</h2>
  <div class="total"><span class="big">&euro;{r100(grand):,}</span>
    <span class="unit">&nbsp;&asymp; &euro;{r100(grand/GFA):,} per m&sup2; &middot; materials only</span></div>
  {bars}

  <h2>Model quality</h2>
  <div class="quality">
    <div class="score {q_class}">{score}</div>
    <div><span class="word">{q_word} ({score}/100).</span> {q_msg}</div>
  </div>

  <h2>Three things to know</h2>
  <ol>
    <li>{bullets[0]}</li>
    <li>{bullets[1]}</li>
    <li>{bullets[2]}</li>
  </ol>

  <footer>
    <span>{PROJECT} &middot; suburban 2-unit duplex</span>
    <span>Indicative design estimate &mdash; not a tender bill of quantities</span>
  </footer>
</div></body></html>
"""

with open("outputs/03-client-report.html", "w") as fh:
    fh.write(html)

print(f"score={score} grand={r100(grand):,} per_m2={r100(grand/GFA)} open_pct={open_pct} fin_pct={fin_pct}")
print("trades:", {t: r100(v) for t, v in trade.items()})
