"""Man Utd 0-3 Bournemouth (25 Oct 2026). Derived numbers from ESPN shot data. Rerun: python3 analysis.py"""
import json, re
S = json.load(open("shots_espn.json"))["shots"]
def minute(s): return int(re.match(r"(\d+)", s["minute"]).group(1))
def agg(team, lo, hi):
    sh = [s for s in S if s["team"] == team and lo <= minute(s) <= hi]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2), "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh),
            "blocked": sum(s["outcome"] == "Blocked" for s in sh)}
out = {"MAN_1st": agg("MAN", 0, 45), "MAN_2nd": agg("MAN", 46, 99), "BOU_1st": agg("BOU", 0, 45), "BOU_2nd": agg("BOU", 46, 99),
       "MAN_all": agg("MAN", 0, 99), "BOU_all": agg("BOU", 0, 99)}
players = {}
for s in S:
    p = players.setdefault((s["player"], s["team"]), {"shots": 0, "xg": 0, "goals": 0})
    p["shots"] += 1; p["xg"] = round(p["xg"] + s["xg"], 2); p["goals"] += s["outcome"] == "Goal"
out["players_by_xg"] = sorted(([k[0], k[1], v["shots"], v["xg"], v["goals"]] for k, v in players.items()), key=lambda r: -r[3])
json.dump(out, open("derived.json", "w"), indent=1)
print(json.dumps(out, indent=1))
