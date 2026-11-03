"""Atlético 0-2 Bayern (UCL, 2026-11-03). Derives numbers from cached sources only.
Run: python3 data/matches/bayern-munich-atletico-madrid-2026-11-03/analysis.py
Note: ESPN labels Bayern as 'MUN' (logo/alt-text bug); treated as BAY here.
"""
import json, os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
SLUG = "bayern-munich-atletico-madrid-2026-11-03"
shots = json.load(open(f"{ROOT}/data/matches/{SLUG}/shots_espn.json"))["shots"]
for s in shots:
    s["team"] = "BAY" if s["team"] == "MUN" else s["team"]
    m = re.match(r"(\d+)'(?:\+(\d+)')?", s["minute"])
    s["min"] = int(m.group(1)) + (int(m.group(2)) if m.group(2) else 0)
    s["half"] = 1 if s["min"] <= 45 and "+" not in s["minute"] or s["min"] <= 45 else 2

def agg(rows):
    on = [r for r in rows if r["outcome"] in ("Saved", "Goal")]
    return {"shots": len(rows), "on_target": len(on), "goals": sum(r["outcome"] == "Goal" for r in rows),
            "xg": round(sum(r["xg"] for r in rows), 2), "xgot": round(sum(r["xgot"] for r in rows), 2)}

out = {"source": "data/matches/%s/shots_espn.json (ESPN shot map)" % SLUG}
for t in ("ATM", "BAY"):
    rows = [s for s in shots if s["team"] == t]
    out[t] = agg(rows)
    out[t]["first_half"] = agg([s for s in rows if s["half"] == 1])
    out[t]["second_half"] = agg([s for s in rows if s["half"] == 2])
    out[t]["inside_set_piece_xg"] = round(sum(r["xg"] for r in rows if r["situation"] == "From Corner"), 2)

# Atlético drought between their own shots
atm = sorted(s["min"] for s in shots if s["team"] == "ATM")
gaps = [(b - a, a, b) for a, b in zip(atm, atm[1:])]
out["ATM_longest_gap_between_shots"] = max(gaps)  # (minutes, from, to)
out["ATM_shot_minutes"] = atm
out["ATM_shots_after_bayern_opener_54"] = agg([s for s in shots if s["team"] == "ATM" and s["min"] > 54])

# players
def player(name, team="BAY"):
    rows = [s for s in shots if s["team"] == team and s["player"] == name]
    return {"shots": len(rows), "on_target": sum(r["outcome"] in ("Saved", "Goal") for r in rows),
            "goals": sum(r["outcome"] == "Goal" for r in rows), "xg": round(sum(r["xg"] for r in rows), 2),
            "minutes": [r["minute"] for r in rows]}
out["Kane"] = player("H. Kane"); out["Laimer"] = player("K. Laimer"); out["Karl"] = player("L. Karl")
out["G_Simeone"] = player("G. Simeone", "ATM")

# cross-check against the cached ESPN team-stats and BBC pages
def cached(key):
    d = f"{ROOT}/data/research"
    for f in os.listdir(d):
        if f.startswith("scrape_"):
            j = json.load(open(f"{d}/{f}"))
            if j["key"] == key:
                return f, j["data"]["markdown"]
espn_file, espn = cached("https://www.espn.com/soccer/team-stats/_/gameId/401915386")
bbc_file, bbc = cached("https://www.bbc.com/sport/football/live/cmy0r2lw77r1t")
checks = {
  "ESPN shots 9 v 19": "9Shots19" in espn, "ESPN SOT 3 v 5": "3Shots on Goal5" in espn,
  "ESPN big chances 2 v 3": "2Big Chances Created3" in espn,
  "BBC xG 0.83 v 1.77": "Atlético Madrid 0.8321Bayern Munich 1.7747" in bbc, "BBC possession 41.5 v 58.5": "41.5%Bayern Munich 58.5%" in bbc,
  "BBC fouls 13 v 3": "Atlético Madrid 13Bayern Munich 3" in bbc,
  "BBC box touches 28 v 38": "Atlético Madrid 28Bayern Munich 38" in bbc,
  "BBC final-third passes 74 v 207": "Atlético Madrid 74Bayern Munich 207" in bbc,
  "BBC Kane rating 8.80": bool(re.search(r"H\. Kane\s+Average Rating: 8\.80", bbc)),
  "BBC G. Simeone rating 3.48": bool(re.search(r"G\. Simeone\s+Average Rating: 3\.48", bbc)),
  "shot map totals match ESPN": out["ATM"]["shots"] == 9 and out["BAY"]["shots"] == 19 and out["ATM"]["on_target"] == 3 and out["BAY"]["on_target"] == 5,
  "shot-map xG sums (BAY 1.78 vs reported 1.77: per-shot rounding; use reported 1.77)": (out["ATM"]["xg"], out["BAY"]["xg"]),
}
out["checks"] = {k: v for k, v in checks.items()}
out["cache_files"] = {"espn_team_stats": espn_file, "bbc": bbc_file}
json.dump(out, open(f"{ROOT}/data/matches/{SLUG}/derived.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
