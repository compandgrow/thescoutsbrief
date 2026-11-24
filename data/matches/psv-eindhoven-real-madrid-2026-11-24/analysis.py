"""Real Madrid 5-1 PSV Eindhoven (UCL, 24 Nov 2026). Derived numbers from the ESPN shot map. Rerun: python3 analysis.py
Half split: first half = minutes <= 45 (incl. 45'+N stoppage), second half = 46+.
Real Madrid's triple half-time change (Bellingham, Huijsen, Konate on at 46') makes the half split = pre/post substitution split."""
import json, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open("shots_espn.json"))["shots"]
def minute(s): return int(re.match(r"(\d+)", s["minute"]).group(1))
def agg(team, lo, hi):
    sh = [s for s in S if s["team"] == team and lo <= minute(s) <= hi]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2),
            "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh),
            "goals": sum(s["outcome"] == "Goal" for s in sh),
            "blocked": sum(s["outcome"] == "Blocked" for s in sh)}
out = {"RMA_1st": agg("RMA", 0, 45), "RMA_2nd": agg("RMA", 46, 99),
       "PSV_1st": agg("PSV", 0, 45), "PSV_2nd": agg("PSV", 46, 99),
       "RMA_all": agg("RMA", 0, 99), "PSV_all": agg("PSV", 0, 99)}
players = {}
for s in S:
    p = players.setdefault((s["player"], s["team"]), {"shots": 0, "xg": 0, "goals": 0, "xgot": 0})
    p["shots"] += 1; p["xg"] = round(p["xg"] + s["xg"], 2); p["xgot"] = round(p["xgot"] + s["xgot"], 2)
    p["goals"] += s["outcome"] == "Goal"
out["players_by_xg"] = sorted(([k[0], k[1], v["shots"], v["xg"], v["xgot"], v["goals"]] for k, v in players.items()), key=lambda r: -r[3])
out["goals"] = [[s["n"], s["player"], s["team"], s["minute"], s["xg"], s["situation"]] for s in S if s["outcome"] == "Goal"]
json.dump(out, open("derived.json", "w"), indent=1)
print(json.dumps(out, indent=1))
