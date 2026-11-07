"""Leeds 1-0 Spurs (7 Nov 2026). Rerun: python3 analysis.py"""
import json
S = json.load(open("shots_espn.json"))["shots"]
out = {}
for t in ("LEE", "TOT"):
    sh = [s for s in S if s["team"] == t]
    out[t] = {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2), "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh)}
out["goals"] = [[s["player"], s["team"], s["minute"], s["xg"]] for s in S if s["outcome"] == "Goal"]
out["Okafor"] = {"shots": sum(s["player"] == "N. Okafor" for s in S), "xg": [s["xg"] for s in S if s["player"] == "N. Okafor"]}
json.dump(out, open("derived.json", "w"), indent=1); print(json.dumps(out))
