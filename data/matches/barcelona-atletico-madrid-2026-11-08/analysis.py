"""Atletico Madrid 1-2 Barcelona (8 Nov 2026). Derived numbers from ESPN shot map. Rerun: python3 analysis.py"""
import json, re
S = json.load(open("shots_espn.json"))["shots"]
def minute(s):
    m = re.match(r"(\d+)(?:'\+(\d+))?", s["minute"]); return int(m.group(1)), int(m.group(2) or 0)
def half(s):
    base, extra = minute(s)
    return 1 if base <= 45 else 2   # 45'+N is first-half stoppage time
def agg(team, h=None, after=None):
    sh = [s for s in S if s["team"] == team and (h is None or half(s) == h) and (after is None or minute(s)[0] > after)]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2),
            "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh),
            "blocked": sum(s["outcome"] == "Blocked" for s in sh),
            "goals": sum(s["outcome"] == "Goal" for s in sh)}
out = {}
for t in ("ATM", "BAR"):
    out[t] = {"all": agg(t), "1st": agg(t, 1), "2nd": agg(t, 2), "after_45": agg(t, after=45)}
players = {}
for s in S:
    p = players.setdefault((s["player"], s["team"]), {"shots": 0, "xg": 0, "goals": 0, "sot": 0})
    p["shots"] += 1; p["xg"] = round(p["xg"] + s["xg"], 2); p["goals"] += s["outcome"] == "Goal"
    p["sot"] += s["outcome"] in ("Saved", "Goal")
out["players_by_xg"] = sorted(([k[0], k[1], v["shots"], v["xg"], v["goals"], v["sot"]] for k, v in players.items()), key=lambda r: -r[3])
# last ATM shot on target
out["ATM_last_on_target_minute"] = [s["minute"] for s in S if s["team"] == "ATM" and s["outcome"] in ("Saved", "Goal")][-1]
out["ATM_xg_in_10th_to_38th_vs_rest"] = None
json.dump(out, open("derived.json", "w"), indent=1)
print(json.dumps(out, indent=1))
