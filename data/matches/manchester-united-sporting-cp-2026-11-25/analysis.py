"""Sporting CP 2-2 Manchester United (UCL, 25 Nov 2026). Derived numbers from the ESPN shot map. Rerun: python3 analysis.py
shots_espn.json has 17 of ESPN's 18 shots; shot 18 (N. Irankunda, SCP, 90'+5', xG 0.02, xGOT 0.00, Off Target, Fast Break)
is added from the cached ESPN match page (data/research/scrape_ca3883766b8d.json, Shot Map '18 of 18').
Half split: first half = minutes <= 45 (incl. stoppage), second half = 46+."""
import json, re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open("shots_espn.json"))["shots"]
if len(S) == 17:
    S.append({"n": 18, "outcome": "Off Target", "player": "N. Irankunda", "team": "SCP", "minute": "90'+5'", "xg": 0.02, "xgot": 0.0, "situation": "Fast Break"})
def minute(s): return int(re.match(r"(\d+)", s["minute"]).group(1))
def agg(sh):
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2),
            "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh),
            "goals": sum(s["outcome"] == "Goal" for s in sh)}
out = {}
for t in ("SCP", "MAN"):
    ts = [s for s in S if s["team"] == t]
    out[f"{t}_all"] = agg(ts)
    out[f"{t}_1st"] = agg([s for s in ts if minute(s) <= 45])
    out[f"{t}_2nd"] = agg([s for s in ts if minute(s) >= 46])
    out[f"{t}_pens"] = agg([s for s in ts if s["situation"] == "Penalty"])
    out[f"{t}_non_pen"] = agg([s for s in ts if s["situation"] != "Penalty"])
# Lammens' error chain: the 33' penalty he conceded + the 80' goal after he dropped the cross
err = [s for s in S if s["team"] == "SCP" and (s["minute"] in ("33'", "80'"))]
out["SCP_xg_from_lammens_errors"] = {"shots": [[s["n"], s["minute"], s["xg"], s["xgot"], s["outcome"]] for s in err],
                                     "xg": round(sum(s["xg"] for s in err), 2)}
out["goals"] = [[s["n"], s["player"], s["team"], s["minute"], s["xg"], s["xgot"], s["situation"]] for s in S if s["outcome"] == "Goal"]
players = {}
for s in S:
    p = players.setdefault((s["player"], s["team"]), {"shots": 0, "xg": 0, "goals": 0})
    p["shots"] += 1; p["xg"] = round(p["xg"] + s["xg"], 2); p["goals"] += s["outcome"] == "Goal"
out["players_by_xg"] = sorted(([k[0], k[1], v["shots"], v["xg"], v["goals"]] for k, v in players.items()), key=lambda r: -r[3])
json.dump(out, open("derived.json", "w"), indent=1)
print(json.dumps(out, indent=1))
