"""Bayern Munich 1-1 FC Cologne (20 Nov 2026). Derived numbers from the ESPN shot map (shots_espn.json).
ESPN labels Bayern 'MUN', Cologne 'KOE'. Rerun: python3 analysis.py"""
import json, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open("shots_espn.json"))["shots"]

def minute(s):  # 45'+4' -> 45 (stoppage stays in its half)
    return int(re.match(r"(\d+)", s["minute"]).group(1))

def agg(team, lo, hi):
    sh = [s for s in S if s["team"] == team and lo <= minute(s) <= hi]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2),
            "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh),
            "blocked": sum(s["outcome"] == "Blocked" for s in sh),
            "off_target": sum(s["outcome"] == "Off Target" for s in sh),
            "goals": sum(s["outcome"] == "Goal" for s in sh),
            "xgot_on_target": round(sum(s["xgot"] for s in sh), 2)}

out = {"BAY_1H": agg("MUN", 0, 45), "BAY_2H": agg("MUN", 46, 99), "KOE_1H": agg("KOE", 0, 45), "KOE_2H": agg("KOE", 46, 99),
       "BAY_all": agg("MUN", 0, 99), "KOE_all": agg("KOE", 0, 99),
       # Kane off 20' (ESPN subs). Bayern before / after.
       "BAY_before_20": agg("MUN", 0, 19), "BAY_from_20": agg("MUN", 20, 99)}
bay = [s for s in S if s["team"] == "MUN"]
koe = [s for s in S if s["team"] == "KOE"]
out["BAY_best_single_chance_xg"] = max(s["xg"] for s in bay)
out["BAY_shots_under_0.10_xg"] = sum(s["xg"] < 0.10 for s in bay)
out["KOE_fast_break"] = {"shots": sum(s["situation"] == "Fast Break" for s in koe),
                         "xg": round(sum(s["xg"] for s in koe if s["situation"] == "Fast Break"), 2)}
out["KOE_moore"] = {"shots": sum(s["player"] == "M. Moore" for s in S),
                    "xg": round(sum(s["xg"] for s in S if s["player"] == "M. Moore"), 2)}
out["BAY_xg_per_shot"] = round(out["BAY_all"]["xg"] / out["BAY_all"]["shots"], 3)
out["KOE_xg_per_shot"] = round(out["KOE_all"]["xg"] / out["KOE_all"]["shots"], 3)
players = {}
for s in S:
    p = players.setdefault((s["player"], s["team"]), {"shots": 0, "xg": 0, "goals": 0, "on_target": 0})
    p["shots"] += 1; p["xg"] = round(p["xg"] + s["xg"], 2); p["goals"] += s["outcome"] == "Goal"
    p["on_target"] += s["outcome"] in ("Goal", "Saved")
out["players_by_xg"] = sorted(([k[0], k[1], v["shots"], v["xg"], v["goals"], v["on_target"]] for k, v in players.items()),
                              key=lambda r: -r[3])
# cross-checks against ESPN team stats page (scrape_fb37c40bdf78.json): shots 17 v 7, on goal 1 v 4, blocked 5 v 1
out["check"] = {"BAY_shots_map_vs_team_stats": [out["BAY_all"]["shots"], 17], "KOE_shots_map_vs_team_stats": [out["KOE_all"]["shots"], 7],
                "BAY_on_target": [out["BAY_all"]["on_target"], 1], "KOE_on_target": [out["KOE_all"]["on_target"], 4],
                "BAY_blocked": [out["BAY_all"]["blocked"], 5], "KOE_blocked": [out["KOE_all"]["blocked"], 1],
                "xg_sum_vs_header": [[out["BAY_all"]["xg"], 1.07], [out["KOE_all"]["xg"], 1.99]]}
json.dump(out, open("derived.json", "w"), indent=1)
print(json.dumps(out, indent=1))
