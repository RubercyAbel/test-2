#!/usr/bin/env python3
"""Génère un panneau HTML de consommation de tokens à partir des transcripts Claude Code.

Lit les fichiers ~/.claude/projects/**/*.jsonl, agrège l'usage par message
(en dédoublonnant les chunks de streaming sur l'id du message) et écrit une
page HTML autonome : totaux, répartition par type de token, par modèle, par
jour et par session.

Usage :
    python3 build_panel.py [--projects DIR] [--out FILE]
"""

import argparse
import html
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

TOKEN_FIELDS = (
    "input_tokens",
    "cache_creation_input_tokens",
    "cache_read_input_tokens",
    "output_tokens",
)
TOKEN_LABELS = {
    "input_tokens": "Entrée",
    "cache_creation_input_tokens": "Écriture cache",
    "cache_read_input_tokens": "Lecture cache",
    "output_tokens": "Sortie",
}


def load_messages(projects_dir: Path):
    """Retourne {message_id: enregistrement} avec l'usage le plus élevé vu pour chaque message."""
    messages = {}
    for path in projects_dir.rglob("*.jsonl"):
        session = path.stem
        with path.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = entry.get("message") or {}
                usage = msg.get("usage")
                msg_id = msg.get("id")
                if not usage or not msg_id:
                    continue
                record = messages.get(msg_id)
                if record is None:
                    record = {
                        "model": msg.get("model") or "inconnu",
                        "session": session,
                        "timestamp": entry.get("timestamp"),
                        "usage": {f: 0 for f in TOKEN_FIELDS},
                    }
                    messages[msg_id] = record
                for field in TOKEN_FIELDS:
                    record["usage"][field] = max(record["usage"][field], usage.get(field) or 0)
                if not record["timestamp"]:
                    record["timestamp"] = entry.get("timestamp")
    return messages


def add_usage(bucket: dict, usage: dict):
    for field in TOKEN_FIELDS:
        bucket[field] += usage[field]
    bucket["messages"] += 1


def aggregate(messages: dict):
    totals = {f: 0 for f in TOKEN_FIELDS}
    totals["messages"] = 0
    by_model = defaultdict(lambda: {**{f: 0 for f in TOKEN_FIELDS}, "messages": 0})
    by_day = defaultdict(lambda: {**{f: 0 for f in TOKEN_FIELDS}, "messages": 0})
    by_session = defaultdict(lambda: {**{f: 0 for f in TOKEN_FIELDS}, "messages": 0})

    for rec in messages.values():
        add_usage(totals, rec["usage"])
        add_usage(by_model[rec["model"]], rec["usage"])
        add_usage(by_session[rec["session"]], rec["usage"])
        day = (rec["timestamp"] or "")[:10] or "inconnu"
        add_usage(by_day[day], rec["usage"])

    return totals, dict(by_model), dict(by_day), dict(by_session)


def fmt(n: int) -> str:
    return f"{n:,}".replace(",", " ")


def share_bars(rows, total_key_fn):
    """Lignes de barres horizontales proportionnelles, HTML + CSS seuls."""
    grand = sum(total_key_fn(v) for _, v in rows) or 1
    out = []
    for label, values in rows:
        value = total_key_fn(values)
        pct = 100 * value / grand
        out.append(
            f'<div class="bar-row"><span class="bar-label">{html.escape(label)}</span>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{pct:.2f}%"></div></div>'
            f'<span class="bar-value">{fmt(value)} <small>({pct:.1f} %)</small></span></div>'
        )
    return "\n".join(out)


def table(headers, rows):
    head = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in row) + "</tr>"
        for row in rows
    )
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def render(totals, by_model, by_day, by_session, generated_at: str) -> str:
    grand_total = sum(totals[f] for f in TOKEN_FIELDS)
    cards = "".join(
        f'<div class="card"><div class="card-label">{TOKEN_LABELS[f]}</div>'
        f'<div class="card-value">{fmt(totals[f])}</div></div>'
        for f in TOKEN_FIELDS
    )
    type_rows = [(TOKEN_LABELS[f], {"v": totals[f]}) for f in TOKEN_FIELDS]
    type_bars = share_bars(type_rows, lambda v: v["v"])

    model_rows = sorted(by_model.items(), key=lambda kv: -sum(kv[1][f] for f in TOKEN_FIELDS))
    model_bars = share_bars(model_rows, lambda v: sum(v[f] for f in TOKEN_FIELDS))
    model_table = table(
        ["Modèle", "Messages"] + [TOKEN_LABELS[f] for f in TOKEN_FIELDS] + ["Total"],
        [
            [m, fmt(v["messages"])]
            + [fmt(v[f]) for f in TOKEN_FIELDS]
            + [fmt(sum(v[f] for f in TOKEN_FIELDS))]
            for m, v in model_rows
        ],
    )

    day_rows = sorted(by_day.items())
    day_svg = day_chart(day_rows)

    session_rows = sorted(
        by_session.items(), key=lambda kv: -sum(kv[1][f] for f in TOKEN_FIELDS)
    )[:20]
    session_table = table(
        ["Session", "Messages", "Total tokens"],
        [
            [s[:8] + "…", fmt(v["messages"]), fmt(sum(v[f] for f in TOKEN_FIELDS))]
            for s, v in session_rows
        ],
    )

    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Consommation de tokens</title>
<style>
:root {{
  --bg: #f7f7f5; --fg: #1d1d1b; --muted: #6b6b66; --card: #ffffff;
  --line: #e2e2dd; --accent: #c15f3c; --track: #ecebe6;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --bg: #1b1b19; --fg: #eeeeea; --muted: #9a9a93; --card: #252523;
    --line: #3a3a37; --accent: #e08a68; --track: #333330;
  }}
}}
:root[data-theme="dark"] {{
  --bg: #1b1b19; --fg: #eeeeea; --muted: #9a9a93; --card: #252523;
  --line: #3a3a37; --accent: #e08a68; --track: #333330;
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--fg);
  font: 15px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }}
main {{ max-width: 960px; margin: 0 auto; padding: 24px 16px 48px; }}
h1 {{ font-size: 22px; margin: 0 0 4px; }}
h2 {{ font-size: 16px; margin: 0 0 12px; }}
.muted {{ color: var(--muted); font-size: 13px; }}
section {{ background: var(--card); border: 1px solid var(--line); border-radius: 10px;
  padding: 16px; margin-top: 16px; }}
.cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin-top: 16px; }}
.card {{ background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 14px; }}
.card-label {{ color: var(--muted); font-size: 13px; }}
.card-value {{ font-size: 22px; font-weight: 600; margin-top: 4px; }}
.grand {{ font-size: 28px; font-weight: 700; color: var(--accent); }}
.bar-row {{ display: grid; grid-template-columns: 140px 1fr 200px; gap: 10px; align-items: center; margin: 8px 0; }}
.bar-track {{ background: var(--track); border-radius: 4px; height: 12px; overflow: hidden; }}
.bar-fill {{ background: var(--accent); height: 100%; }}
.bar-label, .bar-value {{ font-size: 13px; }}
.bar-value small {{ color: var(--muted); }}
table {{ width: 100%; border-collapse: collapse; font-size: 13px; display: block; overflow-x: auto; }}
th, td {{ text-align: right; padding: 6px 8px; border-bottom: 1px solid var(--line); white-space: nowrap; }}
th:first-child, td:first-child {{ text-align: left; }}
svg {{ width: 100%; height: auto; display: block; }}
@media (max-width: 600px) {{
  .bar-row {{ grid-template-columns: 1fr; gap: 4px; }}
}}
</style>
</head>
<body>
<main>
  <h1>Consommation de tokens</h1>
  <div class="muted">Généré le {html.escape(generated_at)} · {fmt(totals['messages'])} messages uniques</div>
  <div class="grand" style="margin-top:12px">{fmt(grand_total)} <span class="muted" style="font-size:14px">tokens au total</span></div>
  <div class="cards">{cards}</div>

  <section>
    <h2>Répartition par type de token</h2>
    {type_bars}
  </section>

  <section>
    <h2>Répartition par modèle</h2>
    {model_bars}
    <div style="margin-top:16px">{model_table}</div>
  </section>

  <section>
    <h2>Consommation par jour</h2>
    {day_svg}
  </section>

  <section>
    <h2>Top 20 sessions</h2>
    {session_table}
  </section>
</main>
</body>
</html>
"""


def day_chart(day_rows) -> str:
    if not day_rows:
        return '<p class="muted">Aucune donnée.</p>'
    width, height, pad = 900, 220, 36
    totals = [(d, sum(v[f] for f in TOKEN_FIELDS)) for d, v in day_rows]
    peak = max(t for _, t in totals) or 1
    slot = (width - 2 * pad) / len(totals)
    bar_w = max(4, slot * 0.7)
    bars = []
    for i, (day, value) in enumerate(totals):
        h = (height - 2 * pad) * value / peak
        x = pad + i * slot + (slot - bar_w) / 2
        y = height - pad - h
        bars.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" fill="var(--accent)">'
            f"<title>{html.escape(day)} : {fmt(value)} tokens</title></rect>"
        )
        if len(totals) <= 15 or i % max(1, len(totals) // 10) == 0:
            bars.append(
                f'<text x="{x + bar_w / 2:.1f}" y="{height - pad + 16}" font-size="11" '
                f'text-anchor="middle" fill="var(--muted)">{html.escape(day[5:])}</text>'
            )
    axis = f'<line x1="{pad}" y1="{height - pad}" x2="{width - pad}" y2="{height - pad}" stroke="var(--line)"/>'
    return (
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="Tokens par jour">'
        f"{axis}{''.join(bars)}</svg>"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--projects", type=Path, default=Path.home() / ".claude" / "projects")
    parser.add_argument("--out", type=Path, default=Path("token_usage_panel.html"))
    args = parser.parse_args()

    messages = load_messages(args.projects)
    totals, by_model, by_day, by_session = aggregate(messages)
    page = render(totals, by_model, by_day, by_session, datetime.now().strftime("%Y-%m-%d %H:%M"))
    args.out.write_text(page, encoding="utf-8")
    print(f"{len(messages)} messages analysés -> {args.out}")


if __name__ == "__main__":
    main()
