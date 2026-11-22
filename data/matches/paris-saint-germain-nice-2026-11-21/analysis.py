"""Nice 2-3 Paris Saint-Germain (21 Nov 2026). Derived numbers from the ESPN shot map (shots_espn.json).
ESPN labels: 'NICE', 'PSG'. Rerun: python3 analysis.py"""
import json, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open("shots_espn.json"))["shots"]

def minute(s):  # 45'+6' -> 45, 90'+5' -> 90 (stoppage stays in its half)
    return int(re.match(r"(\d+)", s["minute"]).group(1))

def agg(team, lo, hi, stoppage=None):
    sh = [s for s in S if s["team"] == team and lo <= minute(s) <= hi]
    if stoppage is not None:
        sh = [s for s in sh if ("+" in s["minute"]) == stoppage]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2),
            "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh),
            "blocked": sum(s["outcome"] == "Blocked" for s in sh),
            "off_target": sum(s["outcome"] == "Off Target" for s in sh),
            "goals": sum(s["outcome"] == "Goal" for s in sh),
            "xgot": round(sum(s["xgot"] for s in sh), 2)}

out = {"NICE_all": agg("NICE", 0, 99), "PSG_all": agg("PSG", 0, 99),
       "NICE_1H": agg("NICE", 0, 45), "NICE_2H": agg("NICE", 46, 99),
       "PSG_1H": agg("PSG", 0, 45), "PSG_2H": agg("PSG", 46, 99),
       "NICE_90_stoppage": agg("NICE", 90, 90, stoppage=True),
       # Doué off injured 44' (Torres on); Dembélé on 61'
       "PSG_before_44": agg("PSG", 0, 43), "PSG_from_44": agg("PSG", 44, 99)}
nice = [s for s in S if s["team"] == "NICE"]
psg = [s for s in S if s["team"] == "PSG"]
# Nice shot timeline: minutes of each Nice shot, and the gap between the 1st and 2nd
out["NICE_shot_minutes"] = [s["minute"] for s in nice]
out["NICE_gap_between_first_and_second_shot"] = {"from": nice[0]["minute"], "to": nice[1]["minute"],
                                                 "note": "no Nice shot between these minutes (shot map has all 4 Nice shots = ESPN team stats total)"}
out["NICE_goals_per_shot"] = f'{out["NICE_all"]["goals"]}/{out["NICE_all"]["shots"]}'
out["PSG_goals_per_shot"] = f'{out["PSG_all"]["goals"]}/{out["PSG_all"]["shots"]}'
out["PSG_best_single_chance_xg"] = max(s["xg"] for s in psg)
out["PSG_shots_under_0.10_xg"] = sum(s["xg"] < 0.10 for s in psg)
out["PSG_outside_box_from_team_stats"] = 7
players = {}
for s in S:
    p = players.setdefault((s["player"], s["team"]), {"shots": 0, "xg": 0, "goals": 0, "on_target": 0, "xgot": 0})
    p["shots"] += 1; p["xg"] = round(p["xg"] + s["xg"], 2); p["goals"] += s["outcome"] == "Goal"
    p["on_target"] += s["outcome"] in ("Goal", "Saved"); p["xgot"] = round(p["xgot"] + s["xgot"], 2)
out["players_by_xg"] = sorted(([k[0], k[1], v["shots"], v["xg"], v["goals"], v["on_target"], v["xgot"]] for k, v in players.items()),
                              key=lambda r: -r[3])
# Goalkeepers: on-target shots faced and the xGOT of them (from the opponent's on-target shots)
for gk, opp in (("Safonov (PSG)", nice), ("Diouf (NICE)", psg)):
    ot = [s for s in opp if s["outcome"] in ("Saved", "Goal")]
    out[f"GK {gk}"] = {"on_target_faced": len(ot), "conceded": sum(s["outcome"] == "Goal" for s in ot),
                       "xgot_faced": round(sum(s["xgot"] for s in ot), 2)}
# cross-checks against ESPN team stats page (scrape_63ddce9ab04f.json): shots 4 v 14, on goal 3 v 5, blocked 1 v 1
out["check"] = {"NICE_shots_map_vs_team_stats": [out["NICE_all"]["shots"], 4], "PSG_shots_map_vs_team_stats": [out["PSG_all"]["shots"], 14],
                "NICE_on_target": [out["NICE_all"]["on_target"], 3], "PSG_on_target": [out["PSG_all"]["on_target"], 5],
                "NICE_blocked": [out["NICE_all"]["blocked"], 1], "PSG_blocked": [out["PSG_all"]["blocked"], 1],
                "xg_sum_vs_header": [[out["NICE_all"]["xg"], 0.78], [out["PSG_all"]["xg"], 1.90]]}
json.dump(out, open("derived.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
