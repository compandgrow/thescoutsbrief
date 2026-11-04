"""Derived numbers from shots_espn.json (ESPN shot map). Rerun: python3 analysis.py"""
import json, re, collections
S = json.load(open("shots_espn.json"))["shots"]
def m(s): return int(re.match(r"(\d+)", s["minute"]).group(1))
out = {}
for t in sorted({s["team"] for s in S}):
    sh = [s for s in S if s["team"] == t]
    out[t] = {"shots": len(sh), "xg_sum": round(sum(s["xg"] for s in sh), 2), "goals": sum(s["outcome"] == "Goal" for s in sh),
              "goal_xg": round(sum(s["xg"] for s in sh if s["outcome"] == "Goal"), 2)}
pl = collections.defaultdict(lambda: [0, 0.0, 0])
for s in S:
    p = pl[(s["player"], s["team"])]; p[0] += 1; p[1] = round(p[1] + s["xg"], 2); p[2] += s["outcome"] == "Goal"
out["players"] = sorted(([k[0], k[1], *v] for k, v in pl.items()), key=lambda r: -r[3])[:8]
out["goals"] = [[s["player"], s["team"], s["minute"], s["xg"], s["xgot"], s["situation"]] for s in S if s["outcome"] == "Goal"]
json.dump(out, open("derived.json", "w"), indent=1); print(json.dumps(out))
