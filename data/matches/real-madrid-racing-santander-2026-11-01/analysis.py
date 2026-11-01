"""Racing 0-3 Real Madrid (1 Nov 2026). Derived from shots_espn.json. Rerun: python3 analysis.py"""
import json, re
S = json.load(open("shots_espn.json"))["shots"]
def minute(s): return int(re.match(r"(\d+)", s["minute"]).group(1))
def agg(team, lo, hi):
    sh = [s for s in S if s["team"] == team and lo <= minute(s) <= hi]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2), "xgot": round(sum(s["xgot"] for s in sh), 2),
            "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh), "goals": sum(s["outcome"] == "Goal" for s in sh)}
out = {k: agg(t, lo, hi) for k, (t, lo, hi) in {"RMA_0_36": ("RMA", 0, 36), "RMA_37_99": ("RMA", 37, 99), "RMA_all": ("RMA", 0, 99), "RAC_all": ("RAC", 0, 99), "RAC_37_99": ("RAC", 37, 99)}.items()}
pl = {}
for s in S:
    p = pl.setdefault((s["player"], s["team"]), {"shots": 0, "xg": 0, "goals": 0})
    p["shots"] += 1; p["xg"] = round(p["xg"] + s["xg"], 2); p["goals"] += s["outcome"] == "Goal"
out["players_by_xg"] = sorted(([k[0], k[1], v["shots"], v["xg"], v["goals"]] for k, v in pl.items()), key=lambda r: -r[3])[:6]
json.dump(out, open("derived.json", "w"), indent=1); print(json.dumps(out, indent=1))
