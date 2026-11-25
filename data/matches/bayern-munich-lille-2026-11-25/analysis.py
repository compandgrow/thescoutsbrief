"""Lille 2-1 Bayern Munich (UCL, 25 Nov 2026). Derived numbers from the ESPN shot map + BBC match momentum.
Rerun: python3 analysis.py  (writes derived.json next to this file)
Half split: first half = minutes <= 45 (incl. 45'+N), second half = 46+.
Shot n=17 is Pavlovic's own goal (listed as team MUN in the ESPN shot map): counted as a Lille goal, excluded
from Bayern's shots and xG (ESPN team stats give Bayern 12 shots without it)."""
import json, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
S = json.load(open(os.path.join(HERE, "shots_espn.json")))["shots"]
OG = [s for s in S if s["situation"] == "Own Goal"]
SH = [s for s in S if s["situation"] != "Own Goal"]


def minute(s):
    m = re.match(r"(\d+)'(?:\+(\d+))?", s["minute"])
    return int(m.group(1))


def agg(team, lo, hi):
    sh = [s for s in SH if s["team"] == team and lo <= minute(s) <= hi]
    return {"shots": len(sh), "xg": round(sum(s["xg"] for s in sh), 2),
            "on_target": sum(s["outcome"] in ("Saved", "Goal") for s in sh),
            "goals": sum(s["outcome"] == "Goal" for s in sh),
            "blocked": sum(s["outcome"] == "Blocked" for s in sh),
            "open_play_xg": round(sum(s["xg"] for s in sh if s["situation"] in ("Regular Play", "Fast Break")), 2)}


out = {"LIL_1st": agg("LILL", 0, 45), "LIL_2nd": agg("LILL", 46, 99),
       "BAY_1st": agg("MUN", 0, 45), "BAY_2nd": agg("MUN", 46, 99),
       "LIL_all": agg("LILL", 0, 99), "BAY_all": agg("MUN", 0, 99),
       # after Bayern's 15' opener until full time
       "BAY_after_goal_16_on": agg("MUN", 16, 99), "LIL_after_goal_16_on": agg("LILL", 16, 99),
       # Kompany's triple change at 76'
       "BAY_46_75": agg("MUN", 46, 75), "BAY_76_on": agg("MUN", 76, 99),
       "LIL_46_75": agg("LILL", 46, 75), "LIL_76_on": agg("LILL", 76, 99)}
out["own_goal"] = [[s["n"], s["player"], s["minute"], "counted for Lille"] for s in OG]
out["goals"] = [[s["n"], s["player"], s["team"], s["minute"], s["xg"], s["xgot"], s["situation"]] for s in SH if s["outcome"] == "Goal"]
out["biggest_chances"] = sorted(([s["n"], s["player"], s["team"], s["minute"], s["xg"], s["outcome"]] for s in SH), key=lambda r: -r[4])[:6]
# Bayern shots by situation
sit = {}
for s in SH:
    if s["team"] == "MUN":
        d = sit.setdefault(s["situation"], {"shots": 0, "xg": 0})
        d["shots"] += 1; d["xg"] = round(d["xg"] + s["xg"], 2)
out["BAY_by_situation"] = sit
players = {}
for s in SH:
    p = players.setdefault((s["player"], s["team"]), {"shots": 0, "xg": 0, "goals": 0, "xgot": 0})
    p["shots"] += 1; p["xg"] = round(p["xg"] + s["xg"], 2); p["xgot"] = round(p["xgot"] + s["xgot"], 2)
    p["goals"] += s["outcome"] == "Goal"
out["players_by_xg"] = sorted(([k[0], k[1], v["shots"], v["xg"], v["xgot"], v["goals"]] for k, v in players.items()), key=lambda r: -r[3])

# BBC match momentum: which team had the most threat in each minute
bbc = json.load(open(os.path.join(ROOT, "data/research/scrape_6edca76f0775.json")))["data"]["markdown"]
rows = re.findall(r"\|\s*(?:KOKick off<br>|HTHalf time<br>|FTFull time<br>)?(\d+)'(?:\+(\d+))?\s*\|\s*(Lille|Bayern Munich)<br>", bbc)
mom = [(int(m), int(st or 0), t) for m, st, t in rows]
seen, uniq = set(), []
for r in mom:                       # the page repeats the table; keep the first copy
    if (r[0], r[1]) in seen:
        break
    seen.add((r[0], r[1])); uniq.append(r)


def count(lo, hi):
    sel = [t for m, st, t in uniq if lo <= m <= hi]
    return {"Lille": sel.count("Lille"), "Bayern Munich": sel.count("Bayern Munich"), "minutes": len(sel)}


out["momentum"] = {"1st_half": count(0, 45), "2nd_half": count(46, 99),
                   "46_75": count(46, 75), "76_on": count(76, 99)}
# longest unbroken Lille run
best, cur, start = (0, None, None), 0, None
for m, st, t in uniq:
    if t == "Lille":
        cur += 1; start = start if cur > 1 else (m, st)
        if cur > best[0]:
            best = (cur, start, (m, st))
    else:
        cur = 0
out["momentum"]["longest_lille_run"] = {"minutes": best[0], "from": best[1], "to": best[2]}
json.dump(out, open(os.path.join(HERE, "derived.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
