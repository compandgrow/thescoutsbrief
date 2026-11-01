"""Bayern 2-2 Dortmund (31 Oct 2026). Derived from ESPN shot data. ESPN tags Bayern as 'MUN' (München) and Dortmund 'DOR'. Rerun: python3 analysis.py"""
import json, re
S = json.load(open("shots_espn.json"))["shots"]
def minute(s): return int(re.match(r"(\d+)", s["minute"]).group(1)) + (0 if "+" not in s["minute"] else 0)
def half(s):
    m = s["minute"]; n = minute(s)
    return 1 if (n < 45 or (n == 45 and "+" in m)) else 2
def agg(team, h=None):
    sh = [s for s in S if s["team"] == team and (h is None or half(s) == h)]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2), "xgot": round(sum(s["xgot"] for s in sh), 2),
            "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh), "goals": sum(s["outcome"] == "Goal" for s in sh)}
out = {k: agg(t, h) for k, (t, h) in {"BAY_all": ("MUN", None), "DOR_all": ("DOR", None), "BAY_1st": ("MUN", 1), "BAY_2nd": ("MUN", 2), "DOR_1st": ("DOR", 1), "DOR_2nd": ("DOR", 2)}.items()}
pl = {}
for s in S:
    p = pl.setdefault((s["player"], s["team"]), {"shots": 0, "xg": 0.0, "goals": 0})
    p["shots"] += 1; p["xg"] = round(p["xg"] + s["xg"], 2); p["goals"] += s["outcome"] == "Goal"
out["players_by_xg"] = sorted(([k[0], k[1], v["shots"], v["xg"], v["goals"]] for k, v in pl.items()), key=lambda r: -r[3])
out["goals"] = [[s["minute"], s["player"], s["team"], s["xg"], s["situation"]] for s in S if s["outcome"] == "Goal"]
out["kane_shots"] = [[s["minute"], s["outcome"], s["xg"], s["situation"]] for s in S if s["player"] == "H. Kane"]
json.dump(out, open("derived.json", "w"), indent=1); print(json.dumps(out, indent=1))
