"""Match data from public pages via Firecrawl (used while PitchAPI isn't connected).

  python3 engine/web_data.py fixtures            -> data/fixtures.json   (refreshes at most once every 6 days; --force)
  python3 engine/web_data.py due                 -> data/queue.json      (watched matches from today/yesterday that have finished)
  python3 engine/web_data.py fetch <espn_game_id> [--bbc <url>] -> data/matches/<slug>/ (match page, team stats, shot map)
  python3 engine/web_data.py form <espn_team_id> [--n 6]          -> data/form/<id>.json  (last results, W/D/L run; 1 credit, cached 6 h)

Sources: ESPN team fixtures/results and match pages, BBC Sport match page (formations, lineups, subs, Opta stats).
Every page is cached by engine/research.py with its URL and fetch time, so the analyst can cite it.
Credit use: ~11 per weekly fixtures refresh, ~1 per finished-match check, ~4 per match fetch.
"""
import argparse, datetime as dt, glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
CFG = json.load(open(os.path.join(ROOT, "config/teams.json")))
ROLE = {t["key"]: t.get("role", "rival") for t in CFG["teams"]}
ESPN_ID = {t["key"]: t.get("espn_id") for t in CFG["teams"]}
NAME = {t["key"]: t["name"] for t in CFG["teams"]}


def research(*args):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "engine/research.py"), *args], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"research.py {args[0]} failed: {(r.stderr or r.stdout).strip()[-400:]}")
    m = re.search(r"saved (\S+\.json)", r.stdout)
    return json.load(open(m.group(1))) if m else None


def cached(url):
    """Most recent cached copy of a URL, if any."""
    best = None
    for f in glob.glob(os.path.join(DATA, "research", "scrape_*.json")):
        x = json.load(open(f))
        if x.get("key") == url and (best is None or x["fetched_at"] > best["fetched_at"]):
            best = x
    return best


def page(url, max_age_min=None):
    c = cached(url)
    if c and max_age_min is not None:
        age = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) - dt.datetime.fromisoformat(c["fetched_at"].rstrip("Z"))
        if age.total_seconds() < max_age_min * 60:
            return c
    return research("scrape", url)


def clean(md):
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    return md


ROW = re.compile(r"\| (\w{3}, \d{1,2} \w{3}) \|(.+?)\|\s*\n")
GAME = re.compile(r"/match/_/gameId/(\d+)/([a-z0-9-]+)")


def parse_table(md, team_key, kind):
    year = dt.date.today().year
    out = []
    for date_s, rest in ROW.findall(clean(md) + "\n"):
        g = GAME.search(rest)
        if not g:
            continue
        cells = [c.strip() for c in ("|" + rest).split("|")]
        names = re.findall(r"\[([^\]]+)\] ?\(?<?https?://[^ )>]*/club/_/id/(\d+)", rest)
        try:
            d = dt.datetime.strptime(f"{date_s} {year}", "%a, %d %b %Y").date()
        except ValueError:
            continue
        if kind == "fixtures" and d < dt.date.today() - dt.timedelta(days=60):
            d = d.replace(year=year + 1)
        comp = next((c for c in reversed(cells) if c and not c.startswith("[") and not re.match(r"^\d", c)), "")
        score = re.search(r"\[(\d+) - (\d+)\]", rest)
        out.append({"espn_id": g.group(1), "slug": g.group(2), "date": d.isoformat(), "team": team_key,
                    "teams_text": [n for n, _ in names if n], "competition": comp.strip(),
                    "score": f"{score.group(1)}-{score.group(2)}" if score else None})
    return out


def cmd_fixtures(force):
    path = os.path.join(DATA, "fixtures.json")
    if os.path.exists(path) and not force:
        age = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) - dt.datetime.fromisoformat(json.load(open(path))["generated"].rstrip("Z"))
        if age.days < 6:
            print(f"fixtures.json is {age.days} days old, not refreshing (use --force)")
            return
    games = {}
    for key, eid in ESPN_ID.items():
        if not eid:
            continue
        p = page(f"https://www.espn.co.uk/football/team/fixtures/_/id/{eid}")
        aliases = next(t["aliases"] + [t["name"]] for t in CFG["teams"] if t["key"] == key)
        headings = re.findall(r"^# (.+)$", p["data"]["markdown"], re.M)
        if not any(a in h for a in aliases for h in headings):
            print(f"WARN: ESPN id {eid} may not be {NAME[key]} (name not found on its page)")
        for g in parse_table(p["data"]["markdown"], key, "fixtures"):
            games.setdefault(g["espn_id"], {**g, "watched": []})["watched"].append(key)
    fx = sorted(games.values(), key=lambda g: g["date"])
    json.dump({"generated": dt.datetime.now(dt.timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds") + "Z", "fixtures": fx}, open(path, "w"), indent=1)
    for g in fx[:40]:
        print(g["date"], g["espn_id"], " v ".join(g["teams_text"]), "|", g["competition"], "| watched:", ",".join(sorted(set(g["watched"]))))


def match_status(eid, slug):
    p = page(f"https://www.espn.co.uk/football/match/_/gameId/{eid}/{slug}", max_age_min=20)
    md = clean(p["data"]["markdown"])
    head = md[:4000]
    lines = [l.strip() for l in clean(md)[:20000].split("\n") if l.strip()]
    # The match header sits just above the "# Home v Away" heading: home score, status (FT / AET / FT-Pens),
    # away score. (League pages also show season records like "1-4-3, 7 PTS"; cup pages don't.)
    # A score ticker of other games can appear above it, so search only the lines right before the heading.
    STATUS = re.compile(r"^(FT|AET|FT-Pens|Pens|Full[- ]?time)\b")
    h = next((i for i, l in enumerate(lines) if l.startswith("# ") and " v " in l), None)
    ft_i, score = None, None
    if h is not None:
        lo = max(0, h - 16)
        st = [i for i in range(lo, h) if STATUS.match(lines[i])]
        if st:
            ft_i = st[-1]
            home = [l for l in lines[lo:ft_i] if re.fullmatch(r"\d{1,2}", l)]
            away = [l for l in lines[ft_i + 1:h] if re.fullmatch(r"\d{1,2}", l)]
            if home and away:
                score = (int(home[-1]), int(away[0]))
    pens = next((l for l in lines[:(h or 0) + 10] if re.search(r"win [\d-]+ on penalties|advances? [\d-]+ on penalties", l)), None)
    if pens:
        score = (score or (0, 0)) + (pens,)
    return ft_i is not None, score, md


def cmd_due():
    fx = json.load(open(os.path.join(DATA, "fixtures.json")))["fixtures"]
    state = json.load(open(os.path.join(DATA, "state.json"))) if os.path.exists(os.path.join(DATA, "state.json")) else {"done": [], "skipped": []}
    done = {str(x.get("espn_id", x)) if isinstance(x, dict) else str(x) for x in state["done"] + state["skipped"]}
    today = dt.date.today()
    window = {(today - dt.timedelta(days=1)).isoformat(), today.isoformat()}
    ready, later, skipped = [], [], []
    for g in fx:
        if g["date"] not in window or g["espn_id"] in done:
            continue
        ft, score, _ = match_status(g["espn_id"], g["slug"])
        keys = sorted(set(g["watched"]))
        item = {**g, "watched": keys, "score": (f"{score[0]}-{score[1]}" + (f" ({score[2]})" if len(score) > 2 else "")) if score else None,
                "favourite_involved": any(ROLE.get(k) == "favourite" for k in keys)}
        if not ft:
            later.append(item)
            continue
        item.update(result_flags(item, score))
        item["make_reel"], item["why"] = should_make(item)
        (ready if item["make_reel"] else skipped).append(item)
    ready.sort(key=lambda g: not g["favourite_involved"])
    cap = CFG.get("automation", {}).get("max_reels_per_run", 3)
    skipped += [{**g, "why": "over the per-run cap, next run"} for g in ready[cap:]]
    ready = ready[:cap]
    json.dump({"generated": dt.datetime.now(dt.timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds") + "Z", "ready": ready, "later_today": later, "not_making": skipped},
              open(os.path.join(DATA, "queue.json"), "w"), indent=1)
    print(f"ready: {len(ready)}  not finished yet: {len(later)}")
    for g in ready:
        print("READY", g["espn_id"], " v ".join(g["teams_text"]), "| fav" if g["favourite_involved"] else "")
    for g in later:
        print("LATER", g["espn_id"], " v ".join(g["teams_text"]))
    for g in skipped:
        print("SKIP ", g["espn_id"], " v ".join(g["teams_text"]), g.get("score"), "|", g.get("why"))


def side_key(team_text):
    """Watched-club key for a team name as ESPN writes it (None if not watched)."""
    t = team_text.lower().replace("é", "e").replace("ü", "u")
    for c in CFG["teams"]:
        for a in c["aliases"] + [c["name"]]:
            a2 = a.lower().replace("é", "e").replace("ü", "u")
            if a2 == t or (len(a2) > 4 and (a2 in t or t in a2)):
                return c["key"]
    return None


def result_flags(g, score):
    if score and len(score) == 3 and len(g["teams_text"]) == 2:      # decided on penalties
        home, away = (side_key(t) for t in g["teams_text"])
        first = score[2].split(" win ")[0].split(" advance")[0].strip()
        win_home = side_key(first) == home if side_key(first) else first.lower() in g["teams_text"][0].lower()
        win, lose = (home, away) if win_home else (away, home)
        return {"winner_key": win, "loser_key": lose, "on_penalties": True,
                "banter": ROLE.get(lose) == "rival",
                "banter_by_favourite": ROLE.get(lose) == "rival" and ROLE.get(win) == "favourite",
                "favourite_lost": ROLE.get(lose) == "favourite"}
    if not score or len(g["teams_text"]) != 2 or score[0] == score[1]:
        return {"winner_key": None, "loser_key": None, "banter": False, "banter_by_favourite": False, "favourite_lost": False}
    home, away = (side_key(t) for t in g["teams_text"])
    win, lose = (home, away) if score[0] > score[1] else (away, home)
    return {"winner_key": win, "loser_key": lose,
            "banter": ROLE.get(lose) == "rival",
            "banter_by_favourite": ROLE.get(lose) == "rival" and ROLE.get(win) == "favourite",
            "favourite_lost": ROLE.get(lose) == "favourite"}


def should_make(g):
    """Which finished matches get a reel (config: automation.reel_rules)."""
    keys = set(g["watched"])
    if any(ROLE.get(k) == "favourite" for k in keys):
        return True, "a favourite played"
    if len(keys) >= 2:
        return True, "two watched clubs met"
    if g.get("banter"):
        return True, "a rival lost (banter)"
    return False, "rival didn't lose to an unwatched club"


def parse_shots(md):
    lines = [l.strip() for l in re.sub(r"\]\(https?://[^)]*\)", "]", clean(md)).split("\n") if l.strip()]
    shots = []
    for i, l in enumerate(lines):
        m = re.match(r"(\d+) of (\d+)$", l)
        if not m:
            continue
        blk = lines[i - 1:i + 24]
        try:
            name = next(b for b in blk if b.startswith("### ")).replace("### [", "").rstrip("]").replace("### ", "")
            team_pos = next(b for b in blk if " • " in b)
            minute = next(b for b in blk if re.match(r"^\d+'(\+\d+')?$", b))
            shots.append({"n": int(m.group(1)), "outcome": lines[i - 1], "player": name, "team": team_pos.split(" • ")[0],
                          "pos": team_pos.split(" • ")[1], "minute": minute, "xg": float(blk[blk.index("xG") - 1]),
                          "xgot": float(blk[blk.index("xGOT") - 1]), "situation": blk[blk.index("Situation") - 1]})
        except (StopIteration, ValueError, IndexError):
            continue
    return shots


def cmd_fetch(eid, bbc):
    fx = {g["espn_id"]: g for g in json.load(open(os.path.join(DATA, "fixtures.json")))["fixtures"]}
    g = fx.get(eid, {"slug": "match", "date": dt.date.today().isoformat(), "teams_text": []})
    slug = f"{g['slug']}-{g['date']}"
    d = os.path.join(DATA, "matches", slug)
    os.makedirs(d, exist_ok=True)
    sources = {}
    mp = page(f"https://www.espn.co.uk/football/match/_/gameId/{eid}/{g['slug']}", max_age_min=30)
    sources["espn_match"] = mp["key"]
    ts = page(f"https://www.espn.com/soccer/team-stats/_/gameId/{eid}")
    sources["espn_team_stats"] = ts["key"]
    shots = parse_shots(mp["data"]["markdown"])
    json.dump({"source": mp["key"], "fetched_at": mp["fetched_at"], "shots": shots}, open(os.path.join(d, "shots_espn.json"), "w"), indent=1)
    if not bbc and len(g["teams_text"]) == 2:
        res = research("search", f"{g['teams_text'][0]} v {g['teams_text'][1]} BBC Sport", "--limit", "3", "--days", "3", "--site", "bbc.com")
        hits = [r["url"] for r in (res or {}).get("data", []) if "/sport/football/live/" in r.get("url", "")]
        bbc = hits[0] if hits else None
    if bbc:
        sources["bbc_match"] = page(bbc)["key"]
    meta = {"espn_id": eid, "slug": slug, "date": g["date"], "teams": g["teams_text"], "competition": g.get("competition"),
            "watched": g.get("watched"), "sources": sources, "shots_parsed": len(shots)}
    json.dump(meta, open(os.path.join(d, "_web_sources.json"), "w"), indent=1)
    print(json.dumps(meta, indent=1))
    if not bbc:
        print("WARN: no BBC match page found (formations/lineups/subs missing); the analyst should search for it.")



RES_ROW = re.compile(r"^\| (\w{3}, \d{1,2} \w{3}) \|(.+)$", re.M)


def cmd_form(team_id, n):
    """Recent results for any club ESPN knows (watched or not), with W/D/L from that club's side."""
    url = f"https://www.espn.co.uk/football/team/results/_/id/{team_id}"
    p = page(url, max_age_min=360)
    md = clean(p["data"]["markdown"])
    today, rows = dt.date.today(), []
    for date_s, rest in RES_ROW.findall(md):
        names = [(nm, i) for nm, i in re.findall(r"\[([^\]]+)\]\(https?://[^ )]*/club/_/id/(\d+)", rest)]
        sc = re.search(r"\[(\d+) - (\d+)\]\(https?://[^ )]*/gameId/(\d+)", rest)
        if not sc or len(names) < 2:
            continue
        (hn, hid), (an, aid) = names[0], names[-1]
        try:
            d = dt.datetime.strptime(f"{date_s} {today.year}", "%a, %d %b %Y").date()
        except ValueError:
            continue
        if d > today:
            d = d.replace(year=today.year - 1)
        hg, ag = int(sc.group(1)), int(sc.group(2))
        home = hid == str(team_id)
        gf, ga = (hg, ag) if home else (ag, hg)
        pens = re.search(r"([A-Z][^|\[\]]*?) (?:win|advance) (\d+)-(\d+) on penalties", rest)
        res = "W" if gf > ga else "L" if gf < ga else "D"
        if pens:
            mine = (hn if home else an).split()[0].lower() in pens.group(1).lower()
            res = "W" if mine else "L"
        cells = [c.strip() for c in rest.split("|")]
        comp = next((c for c in reversed(cells) if c and not c.startswith("[")), "")
        rows.append({"date": d.isoformat(), "opponent": an if home else hn, "venue": "H" if home else "A",
                     "score": f"{gf}-{ga}", "result": res, "pens": bool(pens), "competition": comp,
                     "game_id": sc.group(3)})
    rows = sorted(rows, key=lambda r: r["date"], reverse=True)[:n]
    run = "".join(r["result"] for r in rows)
    gaps = [f"{b['date']} to {a['date']}" for a, b in zip(rows, rows[1:])
            if (dt.date.fromisoformat(a["date"]) - dt.date.fromisoformat(b["date"])).days > 12]
    out = {"team_id": str(team_id), "source": url, "fetched_at": p.get("fetched_at"), "last": rows,
           "run_newest_first": run, "wins": run.count("W"), "draws": run.count("D"), "losses": run.count("L"), "gaps": gaps,
           "note": "Shoot-out results count as W/L for the side that won/lost the shoot-out (pens: true); officially a draw. gaps = more than 12 days between results (international break or missing games): don't claim runs across them without a second source."}
    os.makedirs(os.path.join(DATA, "form"), exist_ok=True)
    json.dump(out, open(os.path.join(DATA, "form", f"{team_id}.json"), "w"), indent=1)
    print(f"form {team_id}: {run} (newest first) from {url}" + (f"  GAPS: {', '.join(gaps)}" if gaps else ""))
    for r in rows:
        print(f"  {r['date']} {r['venue']} {r['result']} {r['score']}{' (pens)' if r['pens'] else ''} v {r['opponent']} | {r['competition']}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fixtures"); f.add_argument("--force", action="store_true")
    sub.add_parser("due")
    m = sub.add_parser("fetch"); m.add_argument("espn_id"); m.add_argument("--bbc")
    fo = sub.add_parser("form"); fo.add_argument("team_id"); fo.add_argument("--n", type=int, default=6)
    a = ap.parse_args()
    {"fixtures": lambda: cmd_fixtures(a.force), "due": cmd_due, "fetch": lambda: cmd_fetch(a.espn_id, a.bbc), "form": lambda: cmd_form(a.team_id, a.n)}[a.cmd]()
