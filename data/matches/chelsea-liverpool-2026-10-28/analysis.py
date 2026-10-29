"""Liverpool 1-1 Chelsea (Liverpool 6-5 pens), Carabao Cup R4, 28 Oct 2026. Derived numbers from the ESPN shot map. Rerun: python3 analysis.py"""
import json, re
S = json.load(open("shots_espn.json"))["shots"]
def minute(s): return int(re.match(r"(\d+)", s["minute"]).group(1))
def is_so(s): return s["situation"] == "Penalty" and minute(s) >= 91   # shootout kicks (no extra time was played)
REG = [s for s in S if not is_so(s)]
SO = [s for s in S if is_so(s)]
def agg(team, lo, hi, pens=True):
    sh = [s for s in REG if s["team"] == team and lo <= minute(s) <= hi and (pens or s["situation"] != "Penalty")]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2), "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh)}
out = {"regulation_shots": len(REG), "shootout_kicks": len(SO), "penalties_total": len(SO) + sum(s["situation"] == "Penalty" for s in REG)}
for t in ("LIV", "CHE"):
    out[t] = {"all": agg(t, 0, 99), "all_non_pen": agg(t, 0, 99, False),
              "1st_half": agg(t, 0, 45), "2nd_half": agg(t, 46, 99),
              "before_59": agg(t, 0, 58), "after_59": agg(t, 59, 99),
              "before_59_non_pen": agg(t, 0, 58, False), "after_59_non_pen": agg(t, 59, 99, False),
              "shootout_scored": sum(s["outcome"] == "Goal" for s in SO if s["team"] == t),
              "shootout_taken": sum(s["team"] == t for s in SO),
              "shootout_kicks": [[s["player"], s["minute"], s["outcome"]] for s in SO if s["team"] == t]}
for t in ("LIV", "CHE"):
    d = out[t]["before_59_non_pen"]; a = out[t]["after_59_non_pen"]
    out[t]["xg_per_shot_before_59_non_pen"] = round(d["xg"] / d["shots"], 2) if d["shots"] else None
    out[t]["xg_per_shot_after_59_non_pen"] = round(a["xg"] / a["shots"], 2) if a["shots"] else None
# keeper "saves": shots on target that were saved in regulation, with post-shot xG of those saves
def saves(shooting_team):
    sv = [s for s in REG if s["team"] == shooting_team and s["outcome"] == "Saved"]
    return {"saves": len(sv), "xgot_saved": round(sum(s["xgot"] for s in sv), 2),
            "on_target_faced": sum(s["outcome"] in ("Saved", "Goal") for s in REG if s["team"] == shooting_team)}
out["Mamardashvili_LIV_GK"] = saves("CHE")
out["Penders_CHE_GK"] = saves("LIV")
# goals in regulation by situation
out["goals_regulation"] = [[s["player"], s["team"], s["minute"], s["situation"]] for s in REG if s["outcome"] == "Goal"]
json.dump(out, open("derived.json", "w"), indent=1)
print(json.dumps(out, indent=1))
