"""Chelsea 1-4 Leeds United (21 Nov 2026). Derived numbers from the ESPN shot map (shots_espn.json).
CHE = Chelsea (home), LEE = Leeds United. Rerun: python3 analysis.py"""
import json, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open("shots_espn.json"))["shots"]


def minute(s):  # 45'+6' -> 45 (stoppage stays in its half)
    return int(re.match(r"(\d+)", s["minute"]).group(1))


def agg(team, lo, hi):
    sh = [s for s in S if s["team"] == team and lo <= minute(s) <= hi]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2),
            "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh),
            "blocked": sum(s["outcome"] == "Blocked" for s in sh),
            "off_target": sum(s["outcome"] == "Off Target" for s in sh),
            "goals": sum(s["outcome"] == "Goal" for s in sh),
            "xgot": round(sum(s["xgot"] for s in sh), 2)}


out = {t + "_" + k: agg(t, lo, hi) for t in ("CHE", "LEE")
       for k, (lo, hi) in {"all": (0, 99), "1H": (0, 45), "2H": (46, 99)}.items()}
# Chelsea led 1-0 at 25' (ESPN). Leeds from the 25' goal onwards.
out["LEE_after_CHE_goal_25"] = agg("LEE", 26, 99)
out["CHE_after_CHE_goal_25"] = agg("CHE", 26, 99)

che = [s for s in S if s["team"] == "CHE"]
lee = [s for s in S if s["team"] == "LEE"]
out["CHE_best_single_chance_xg"] = max(s["xg"] for s in che)
out["CHE_shots_under_0.10_xg"] = sum(s["xg"] < 0.10 for s in che)
out["CHE_xg_per_shot"] = round(out["CHE_all"]["xg"] / out["CHE_all"]["shots"], 3)
out["LEE_xg_per_shot"] = round(out["LEE_all"]["xg"] / out["LEE_all"]["shots"], 3)
# Martinez: goals conceded vs xGOT of Leeds shots on target (goals prevented = xGOT faced - goals conceded)
on = [s for s in lee if s["outcome"] in ("Goal", "Saved")]
out["martinez"] = {"sot_faced": len(on), "goals_conceded": sum(s["outcome"] == "Goal" for s in on),
                   "saves": sum(s["outcome"] == "Saved" for s in on),
                   "xgot_faced": round(sum(s["xgot"] for s in on), 2)}
out["martinez"]["goals_prevented"] = round(out["martinez"]["xgot_faced"] - out["martinez"]["goals_conceded"], 2)
out["martinez_non_penalty"] = {"goals_conceded": sum(s["outcome"] == "Goal" and s["situation"] != "Penalty" for s in on),
                               "xgot_faced": round(sum(s["xgot"] for s in on if s["situation"] != "Penalty"), 2)}

players = {}
for s in S:
    p = players.setdefault((s["player"], s["team"]), {"shots": 0, "xg": 0, "goals": 0, "on_target": 0})
    p["shots"] += 1; p["xg"] = round(p["xg"] + s["xg"], 2); p["goals"] += s["outcome"] == "Goal"
    p["on_target"] += s["outcome"] in ("Goal", "Saved")
out["players_by_xg"] = sorted(([k[0], k[1], v["shots"], v["xg"], v["goals"], v["on_target"]] for k, v in players.items()),
                              key=lambda r: -r[3])
out["goals"] = [[s["player"], s["team"], s["minute"], s["xg"], s["xgot"], s["situation"]] for s in S if s["outcome"] == "Goal"]
# cross-checks vs ESPN team stats (scrape_5ffdcfb0c0e7.json): shots 14 v 21, on goal 3 v 8, blocked 5 v 4; xG 0.56 v 2.51 (BBC + ESPN)
out["check"] = {"CHE_shots": [out["CHE_all"]["shots"], 14], "LEE_shots": [out["LEE_all"]["shots"], 21],
                "CHE_on_target": [out["CHE_all"]["on_target"], 3], "LEE_on_target": [out["LEE_all"]["on_target"], 8],
                "CHE_blocked": [out["CHE_all"]["blocked"], 5], "LEE_blocked": [out["LEE_all"]["blocked"], 4],
                "xg_sum_vs_header": [[out["CHE_all"]["xg"], 0.56], [out["LEE_all"]["xg"], 2.51]]}
json.dump(out, open("derived.json", "w"), indent=1)
print(json.dumps(out, indent=1))
