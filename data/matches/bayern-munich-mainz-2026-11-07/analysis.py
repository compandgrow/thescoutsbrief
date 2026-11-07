"""Mainz 1-2 Bayern (7 Nov 2026). NB ESPN abbreviates Bayern as 'MUN' and Mainz as 'M05' in the shot map. Rerun: python3 analysis.py"""
import json, re
S = json.load(open("shots_espn.json"))["shots"]
def minute(s): return int(re.match(r"(\d+)", s["minute"]).group(1))
def agg(team, lo, hi):
    sh = [s for s in S if s["team"] == team and lo <= minute(s) <= hi]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2), "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh)}
out = {"Mainz_all": agg("M05", 0, 99), "Bayern_all": agg("MUN", 0, 99), "Bayern_1H": agg("MUN", 0, 45), "Bayern_2H": agg("MUN", 46, 99)}
out["goals"] = [[s["player"], s["team"], s["minute"], s["xg"]] for s in S if s["outcome"] == "Goal"]
for n in ("H. Kane", "L. Karl"):
    sh = [s for s in S if s["player"] == n]
    out[n] = {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2), "goals": sum(s["outcome"] == "Goal" for s in sh)}
json.dump(out, open("derived.json", "w"), indent=1); print(json.dumps(out))
