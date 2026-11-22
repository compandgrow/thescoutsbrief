"""Liverpool 4-0 Man Utd (22 Nov 2026, Anfield). Derived numbers from the ESPN shot map (shots_espn.json).
Yoro red card 8' (BBC line-ups 'Red Card at 8 minutes'); Maguire on for Mbeumo 22' (BBC + ESPN line-ups).
Rerun: python3 analysis.py  -> derived.json"""
import json, re
S = json.load(open("shots_espn.json"))["shots"]
def minute(s):
    m = re.match(r"(\d+)'(?:\+(\d+)')?", s["minute"]); return int(m.group(1)) + (int(m.group(2)) / 100 if m.group(2) else 0)
def agg(team, lo, hi):
    sh = [s for s in S if s["team"] == team and lo <= minute(s) < hi]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2), "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh),
            "goals": sum(s["outcome"] == "Goal" for s in sh), "blocked": sum(s["outcome"] == "Blocked" for s in sh)}
W = {"0-8 (11 v 11)": (0, 8), "8-22 (10 men, before Maguire)": (8, 22), "22-45+ (Maguire on)": (22, 46),
     "1st half": (0, 46), "2nd half": (46, 100), "after red (8-FT)": (8, 100), "all": (0, 100)}
out = {f"{t}_{k}": agg(t, *v) for k, v in W.items() for t in ("LIV", "MAN")}
players = {}
for s in S:
    p = players.setdefault((s["player"], s["team"]), {"shots": 0, "xg": 0, "on_target": 0, "goals": 0})
    p["shots"] += 1; p["xg"] = round(p["xg"] + s["xg"], 2); p["on_target"] += s["outcome"] in ("Saved", "Goal"); p["goals"] += s["outcome"] == "Goal"
out["players_by_xg"] = sorted(([k[0], k[1], v["shots"], v["xg"], v["on_target"], v["goals"]] for k, v in players.items()), key=lambda r: -r[3])
out["situations"] = {}
for s in S:
    d = out["situations"].setdefault(f'{s["team"]} {s["situation"]}', {"shots": 0, "xg": 0}); d["shots"] += 1; d["xg"] = round(d["xg"] + s["xg"], 2)
out["goals"] = [[s["minute"], s["player"], s["team"], s["xg"], s["situation"]] for s in S if s["outcome"] == "Goal"]
out["liv_shots_per_10min_after_red"] = round(out["LIV_after red (8-FT)"]["shots"] / ((94 - 8) / 10), 2)  # 90+4 per BBC timeline 'FT 90'+4'
json.dump(out, open("derived.json", "w"), indent=1)
print(json.dumps(out, indent=1))
