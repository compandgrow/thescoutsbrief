"""AS Roma 2-3 Man Utd (UCL, 3 Nov 2026). Derived numbers from the ESPN shot map and ESPN form file.
Rerun from this folder: python3 analysis.py  -> derived.json"""
import json, re
S = json.load(open("shots_espn.json"))["shots"]
FORM = json.load(open("../../form/360.json"))["last"]  # ESPN results for Man Utd, newest first

def minute(s):
    return int(re.match(r"(\d+)", s["minute"]).group(1))
def half(s):  # 45'+n counts as first half
    return 1 if minute(s) <= 45 else 2
def agg(team, h=None, no_pen=False):
    sh = [s for s in S if s["team"] == team and (h is None or half(s) == h) and not (no_pen and s["situation"] == "Penalty")]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2),
            "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh),
            "blocked": sum(s["outcome"] == "Blocked" for s in sh),
            "goals": sum(s["outcome"] == "Goal" for s in sh)}
out = {}
for t in ("MAN", "ROMA"):
    out[t + "_1st"] = agg(t, 1); out[t + "_2nd"] = agg(t, 2); out[t + "_all"] = agg(t)
    out[t + "_2nd_no_pen"] = agg(t, 2, True)
players = {}
for s in S:
    p = players.setdefault((s["player"], s["team"]), {"shots": 0, "xg": 0, "goals": 0, "mins": []})
    p["shots"] += 1; p["xg"] = round(p["xg"] + s["xg"], 2); p["goals"] += s["outcome"] == "Goal"; p["mins"].append(s["minute"])
out["players_by_xg"] = sorted(([k[0], k[1], v["shots"], v["xg"], v["goals"], v["mins"]] for k, v in players.items()), key=lambda r: -r[3])
out["man_goal_minutes"] = [s["minute"] for s in S if s["team"] == "MAN" and s["outcome"] == "Goal"]
out["roma_goal_minutes"] = [s["minute"] for s in S if s["team"] == "ROMA" and s["outcome"] == "Goal"]

# Form before this match: the winless run (ESPN results, all competitions). Skip this match (2026-11-03).
prev = [g for g in FORM if g["date"] < "2026-11-03"]
run = []
for g in prev:
    if g["result"] == "W": break
    run.append(g)
out["winless_run_before_match"] = {"games": len(run), "draws": sum(g["result"] == "D" for g in run),
                                  "losses": sum(g["result"] == "L" for g in run),
                                  "last_win": next(g["date"] + " " + g["score"] + " v " + g["opponent"] for g in prev if g["result"] == "W"),
                                  "competitions": "all"}
json.dump(out, open("derived.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
