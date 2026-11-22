"""Real Madrid 2-1 Celta Vigo (21 Nov 2026, Bernabeu). Derived numbers from the ESPN shot map (shots_espn.json).
RMA = Real Madrid (home), CEL = Celta Vigo. Rerun: python3 analysis.py"""
import json, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open("shots_espn.json"))["shots"]


def minute(s):  # 45'+3' -> 45 (stoppage stays in its half)
    return int(re.match(r"(\d+)", s["minute"]).group(1))


def agg(team, lo, hi, pens=True):
    sh = [s for s in S if s["team"] == team and lo <= minute(s) <= hi and (pens or s["situation"] != "Penalty")]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2),
            "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh),
            "blocked": sum(s["outcome"] == "Blocked" for s in sh),
            "off_target": sum(s["outcome"] == "Off Target" for s in sh),
            "goals": sum(s["outcome"] == "Goal" for s in sh),
            "xgot": round(sum(s["xgot"] for s in sh), 2)}


out = {t + "_" + k: agg(t, lo, hi) for t in ("RMA", "CEL")
       for k, (lo, hi) in {"all": (0, 99), "1H": (0, 45), "2H": (46, 99)}.items()}
# Triple substitution at 57' (Cucurella, Valverde, Vinicius on; ESPN lineups). Shots up to 57' vs after.
out["RMA_before_57"] = agg("RMA", 0, 57)
out["RMA_after_57"] = agg("RMA", 58, 99)
out["CEL_before_57"] = agg("CEL", 0, 57)
out["CEL_after_57"] = agg("CEL", 58, 99)
out["RMA_all_non_penalty"] = agg("RMA", 0, 99, pens=False)
out["RMA_1H_non_penalty"] = agg("RMA", 0, 45, pens=False)
# Celta's 6' goal: share of Celta's xG from one shot
cel_goal = [s for s in S if s["team"] == "CEL" and s["outcome"] == "Goal"][0]
out["CEL_goal_xg"] = cel_goal["xg"]
out["CEL_other_7_shots_xg"] = round(out["CEL_all"]["xg"] - cel_goal["xg"], 2)

players = {}
for s in S:
    p = players.setdefault((s["player"], s["team"]), {"shots": 0, "xg": 0, "goals": 0, "on_target": 0})
    p["shots"] += 1; p["xg"] = round(p["xg"] + s["xg"], 2); p["goals"] += s["outcome"] == "Goal"
    p["on_target"] += s["outcome"] in ("Goal", "Saved")
out["players_by_xg"] = sorted(([k[0], k[1], v["shots"], v["xg"], v["goals"], v["on_target"]] for k, v in players.items()),
                              key=lambda r: -r[3])
out["goals"] = [[s["player"], s["team"], s["minute"], s["xg"], s["xgot"], s["situation"]] for s in S if s["outcome"] == "Goal"]
out["penalty"] = [[s["player"], s["minute"], s["xg"], s["outcome"]] for s in S if s["situation"] == "Penalty"]
# Cross-checks vs ESPN team stats (data/research/scrape_9644e9ecf75e.json): shots 24 v 8, on goal 7 v 4, blocked 8 v 1;
# xG header 3.75 v 1.64 (ESPN match page Team Stats). Use the header numbers on screen.
out["check"] = {"RMA_shots": [out["RMA_all"]["shots"], 24], "CEL_shots": [out["CEL_all"]["shots"], 8],
                "RMA_on_target": [out["RMA_all"]["on_target"], 7], "CEL_on_target": [out["CEL_all"]["on_target"], 4],
                "RMA_blocked": [out["RMA_all"]["blocked"], 8], "CEL_blocked": [out["CEL_all"]["blocked"], 1],
                "xg_sum_vs_header": [[out["RMA_all"]["xg"], 3.75], [out["CEL_all"]["xg"], 1.64]]}
json.dump(out, open("derived.json", "w"), indent=1)
print(json.dumps(out, indent=1))
