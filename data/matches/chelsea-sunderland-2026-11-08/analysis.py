"""Sunderland 1-0 Chelsea (8 Nov 2026). Rerun from the repo root:
python3 data/matches/chelsea-sunderland-2026-11-08/analysis.py
Reads the cached ESPN shot map (shots_espn.json) and the cached BBC match page
(data/research/scrape_c74d96800865.json) and writes derived.json next to this file."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
S = json.load(open(os.path.join(HERE, "shots_espn.json")))["shots"]

def minute(m):
    return int(re.match(r"(\d+)", m).group(1))

def half(s):          # stoppage time of the 1st half is written 45'+N'
    m = s["minute"]
    return 1 if (minute(m) < 45 or (minute(m) == 45)) else 2

out = {}
for t in ("SUN", "CHE"):
    sh = [s for s in S if s["team"] == t]
    out[t] = {
        "shots": len(sh),
        "xg_sum": round(sum(s["xg"] for s in sh), 2),
        "xg_pen": round(sum(s["xg"] for s in sh if s["situation"] == "Penalty"), 2),
        "xg_ex_pen": round(sum(s["xg"] for s in sh if s["situation"] != "Penalty"), 2),
        "h1_shots": sum(half(s) == 1 for s in sh), "h1_xg": round(sum(s["xg"] for s in sh if half(s) == 1), 2),
        "h2_shots": sum(half(s) == 2 for s in sh), "h2_xg": round(sum(s["xg"] for s in sh if half(s) == 2), 2),
        "biggest_chance": max(((s["xg"], s["player"], s["minute"], s["outcome"]) for s in sh)),
    }
out["goal"] = [[s["player"], s["team"], s["minute"], s["xg"], s["situation"]] for s in S if s["outcome"] == "Goal"]
# Brobbey and Le Fee
for p in ("B. Brobbey", "E. Le Fée"):
    out[p] = {"shots": sum(s["player"] == p for s in S), "xg": round(sum(s["xg"] for s in S if s["player"] == p), 2)}
# Chelsea starters: shots and xG
for p in ("M. Rogers", "C. Palmer", "P. Neto", "R. Lavia", "W. Fofana"):
    out[p] = {"shots": sum(s["player"] == p for s in S), "xg": round(sum(s["xg"] for s in S if s["player"] == p), 2)}

# BBC page: team stats (cached text)
bbc = json.load(open(os.path.join(ROOT, "data/research/scrape_c74d96800865.json")))["data"]["markdown"]
def pair(label):
    m = re.search(r"#### " + re.escape(label) + r"\n+Sunderland ([\d.]+)Chelsea ([\d.]+)", bbc)
    return [float(m.group(1)), float(m.group(2))] if m else None
out["bbc_stats"] = {l: pair(l) for l in [
    "Overall possession", "xG", "xG from open play", "xG from set play", "Shots", "Shots on target",
    "Total touches inside the opposition box", "Total passes", "Successful final third passes", "Total crosses",
    "Goalkeeper saves", "Fouls committed", "Total tackles", "One-on-one attempts"]}
m = re.search(r"Sunderland ([\d.]+)%\s*Chelsea ([\d.]+)%", bbc)
out["bbc_stats"]["Overall possession"] = [float(m.group(1)), float(m.group(2))]
json.dump(out, open(os.path.join(HERE, "derived.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
