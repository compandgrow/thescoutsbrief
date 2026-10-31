"""Chelsea 2-0 Man Utd (31 Oct 2026). Derived numbers from ESPN shot map (shots_espn.json).
Shot n=19 (C. Palmer 64' penalty, xG 0.79) is missing from shots_espn.json because ESPN shows 'No shot data' for it;
it is added by hand below from the cached ESPN page (data/research/scrape_f882629d21b4.json, 'C. Palmer 64' 0.79 xG Penalty').
Check: CHE total 1.88 + 0.79 = 2.67 = BBC xG 2.6687. Rerun: python3 analysis.py"""
import json, re
S = json.load(open("shots_espn.json"))["shots"]
S.append({"n": 19, "player": "C. Palmer", "team": "CHE", "minute": "64'", "xg": 0.79, "situation": "Penalty", "outcome": "Goal(pen, per ESPN header)"})
def minute(s):
    m = re.match(r"(\d+)'?(?:\+(\d+))?", s["minute"]); return int(m.group(1)) + (int(m.group(2) or 0) / 100)
def agg(team, lo, hi, pen=True):
    sh = [s for s in S if s["team"] == team and lo <= minute(s) < hi and (pen or s["situation"] != "Penalty")]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2)}
out = {}
for t in ("CHE", "MAN"):
    out[t + "_1st_half"] = agg(t, 0, 45.5)
    out[t + "_2nd_half"] = agg(t, 45.5, 200)
    out[t + "_before_red_0_62"] = agg(t, 0, 63)
    out[t + "_after_red_63+"] = agg(t, 63, 200)
    out[t + "_all"] = agg(t, 0, 200)
    out[t + "_all_ex_pen"] = agg(t, 0, 200, pen=False)
players = {}
for s in S:
    p = players.setdefault((s["player"], s["team"]), {"shots": 0, "xg": 0})
    p["shots"] += 1; p["xg"] = round(p["xg"] + s["xg"], 2)
out["players_by_xg"] = sorted(([k[0], k[1], v["shots"], v["xg"]] for k, v in players.items()), key=lambda r: -r[3])[:8]
json.dump(out, open("derived.json", "w"), indent=1)
print(json.dumps(out, indent=1))
