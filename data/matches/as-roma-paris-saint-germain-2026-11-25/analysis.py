"""Paris Saint-Germain 2-2 AS Roma (UCL, 25 Nov 2026). Derived numbers from the ESPN shot map. Rerun: python3 analysis.py
Half split: first half = minutes <= 45 (incl. 45'+N stoppage), second half = 46+.
PSG double change at 59' (Dembele for Ferran Torres, Zaire-Emery for Nuno Mendes): pre = minute <= 58, post = 59+.
Penalties are split out because both second-half goals were penalties (0.79 xG each)."""
import json, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open("shots_espn.json"))["shots"]


def minute(s):
    return int(re.match(r"(\d+)", s["minute"]).group(1))


def agg(team, lo, hi, pens=True):
    sh = [s for s in S if s["team"] == team and lo <= minute(s) <= hi and (pens or s["situation"] != "Penalty")]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2),
            "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh),
            "goals": sum(s["outcome"] == "Goal" for s in sh),
            "blocked": sum(s["outcome"] == "Blocked" for s in sh)}


out = {}
for t in ("PSG", "ROMA"):
    out[f"{t}_all"] = agg(t, 0, 99)
    out[f"{t}_1st"] = agg(t, 0, 45)
    out[f"{t}_2nd"] = agg(t, 46, 99)
    out[f"{t}_all_nonpen"] = agg(t, 0, 99, pens=False)
    out[f"{t}_pre59"] = agg(t, 0, 58)
    out[f"{t}_post59"] = agg(t, 59, 99)
    out[f"{t}_post59_nonpen"] = agg(t, 59, 99, pens=False)
    sit = {}
    for s in S:
        if s["team"] == t:
            k = sit.setdefault(s["situation"], {"shots": 0, "xg": 0})
            k["shots"] += 1
            k["xg"] = round(k["xg"] + s["xg"], 2)
    out[f"{t}_by_situation"] = sit
players = {}
for s in S:
    p = players.setdefault((s["player"], s["team"]), {"shots": 0, "xg": 0, "goals": 0, "xgot": 0, "on_target": 0})
    p["shots"] += 1
    p["xg"] = round(p["xg"] + s["xg"], 2)
    p["xgot"] = round(p["xgot"] + s["xgot"], 2)
    p["goals"] += s["outcome"] == "Goal"
    p["on_target"] += s["outcome"] in ("Saved", "Goal")
out["players_by_xg"] = sorted(([k[0], k[1], v["shots"], v["on_target"], v["xg"], v["xgot"], v["goals"]] for k, v in players.items()),
                              key=lambda r: -r[4])
out["goals"] = [[s["n"], s["player"], s["team"], s["minute"], s["xg"], s["xgot"], s["situation"]] for s in S if s["outcome"] == "Goal"]
out["biggest_misses"] = [[s["n"], s["player"], s["team"], s["minute"], s["xg"], s["outcome"]]
                         for s in sorted(S, key=lambda s: -s["xg"]) if s["outcome"] != "Goal"][:4]
json.dump(out, open("derived.json", "w"), indent=1)
print(json.dumps(out, indent=1))
