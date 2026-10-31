"""Man City 0-1 Brighton (31 Oct 2026). Derived numbers from ESPN shot map. Rerun: python3 analysis.py"""
import json, re
S = json.load(open("shots_espn.json"))["shots"]
def minute(s): return int(re.match(r"(\d+)", s["minute"]).group(1))
def agg(team, lo, hi):
    sh = [s for s in S if s["team"] == team and lo <= minute(s) <= hi]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2), "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh),
            "blocked": sum(s["outcome"] == "Blocked" for s in sh), "off_target": sum(s["outcome"] == "Off Target" for s in sh)}
out = {}
for t in ("MNC", "BHA"):
    out[t + "_1st"] = agg(t, 0, 45); out[t + "_2nd"] = agg(t, 46, 99); out[t + "_all"] = agg(t, 0, 99)
    out[t + "_after_goal"] = agg(t, 12, 99)
players = {}
for s in S:
    p = players.setdefault((s["player"], s["team"]), {"shots": 0, "xg": 0, "goals": 0})
    p["shots"] += 1; p["xg"] = round(p["xg"] + s["xg"], 2); p["goals"] += s["outcome"] == "Goal"
out["players_by_xg"] = sorted(([k[0], k[1], v["shots"], v["xg"], v["goals"]] for k, v in players.items()), key=lambda r: -r[3])
json.dump(out, open("derived.json", "w"), indent=1)
print(json.dumps(out, indent=1))
