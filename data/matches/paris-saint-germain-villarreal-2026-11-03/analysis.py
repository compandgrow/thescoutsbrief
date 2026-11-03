"""Villarreal 0-6 PSG (3 Nov 2026). Derived numbers from ESPN shot data. Rerun: python3 analysis.py"""
import json, re
S = json.load(open("shots_espn.json"))["shots"]
def minute(s): return int(re.match(r"(\d+)", s["minute"]).group(1))
def agg(team, lo, hi):
    sh = [s for s in S if s["team"] == team and lo <= minute(s) <= hi]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2), "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh),
            "goals": sum(s["outcome"] == "Goal" for s in sh), "blocked": sum(s["outcome"] == "Blocked" for s in sh)}
out = {}
for t in ("VIL", "PSG"):
    out[t + "_first_17min"] = agg(t, 0, 17)
    out[t + "_after_17min"] = agg(t, 18, 120)
    out[t + "_all"] = agg(t, 0, 120)
# stoppage-time shots are tagged 45'+N and read as minute 45, so they count as first half
def half(team, second):
    sh = [s for s in S if s["team"] == team and ((minute(s) > 45) == second)]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2), "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh), "goals": sum(s["outcome"] == "Goal" for s in sh)}
for t in ("VIL", "PSG"):
    out[t + "_1st_half"] = half(t, False)
    out[t + "_2nd_half"] = half(t, True)
players = {}
for s in S:
    p = players.setdefault((s["player"], s["team"]), {"shots": 0, "xg": 0, "goals": 0, "xgot": 0})
    p["shots"] += 1; p["xg"] = round(p["xg"] + s["xg"], 2); p["xgot"] = round(p["xgot"] + s["xgot"], 2); p["goals"] += s["outcome"] == "Goal"
out["players_by_xg"] = sorted(([k[0], k[1], v["shots"], v["xg"], v["goals"], v["xgot"]] for k, v in players.items()), key=lambda r: -r[3])
out["goals"] = [[s["minute"], s["player"], s["team"], s["xg"], s["situation"]] for s in S if s["outcome"] == "Goal"]
out["PSG_goal_shots_xg_first_17"] = round(sum(s["xg"] for s in S if s["team"] == "PSG" and s["outcome"] == "Goal" and minute(s) <= 17), 2)
json.dump(out, open("derived.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
