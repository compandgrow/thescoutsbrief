"""PitchAPI data layer for The Scout Brief.

Needs:  pip install pitchapi   and   PITCHAPI_API_KEY in the environment.
Network: api.pitchapi.dev must be allowed in the cloud environment.

  python3 engine/pitch.py schedule [--days 7]   -> data/fixtures.json  (watchlist fixtures, next N days)
  python3 engine/pitch.py today                 -> data/today.json     (watchlist matches today + status)
  python3 engine/pitch.py fetch <match_id>      -> data/matches/<id>/*.json  (everything for one match)
"""
import argparse, datetime as dt, json, os, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
CFG = json.load(open(os.path.join(ROOT, "config/teams.json")))


def client():
    try:
        from pitchapi import PitchAPI
    except ImportError:
        sys.exit("pitchapi SDK missing: run  pip install pitchapi")
    if not os.environ.get("PITCHAPI_API_KEY"):
        sys.exit("PITCHAPI_API_KEY is not set (add it to the environment's variables)")
    return PitchAPI()


def plain(o, depth=0):
    """SDK model -> plain JSON (works for pydantic, dataclasses, attrs or plain objects)."""
    if depth > 40:
        return str(o)
    if o is None or isinstance(o, (str, int, float, bool)):
        return o
    if isinstance(o, (dt.date, dt.datetime)):
        return o.isoformat()
    if isinstance(o, dict):
        return {str(k): plain(v, depth + 1) for k, v in o.items()}
    if isinstance(o, (list, tuple, set)):
        return [plain(v, depth + 1) for v in o]
    for m in ("model_dump", "to_dict", "dict"):
        f = getattr(o, m, None)
        if callable(f):
            try:
                return plain(f(), depth + 1)
            except TypeError:
                pass
    if hasattr(o, "__dict__"):
        return {k: plain(v, depth + 1) for k, v in vars(o).items() if not k.startswith("_")}
    return str(o)


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return " ".join(s.replace(".", " ").replace("-", " ").split())


ALIASES = {norm(a): t["key"] for t in CFG["teams"] for a in t["aliases"] + [t["name"]]}
ROLE = {t["key"]: t.get("role", "rival") for t in CFG["teams"]}


def team_key(name):
    n = norm(name)
    if n in ALIASES:
        return ALIASES[n]
    for a, k in ALIASES.items():          # e.g. "FC Bayern München" vs "Bayern"
        if len(a) > 4 and (a in n or n in a):
            return k
    return None


def watched(m):
    h, a = team_key(m["home_team"]["name"]), team_key(m["away_team"]["name"])
    if not (h or a):
        return None
    info = {"home_key": h, "away_key": a, "home_role": ROLE.get(h), "away_role": ROLE.get(a),
            "favourite_involved": "favourite" in (ROLE.get(h), ROLE.get(a))}
    sh, sa = m.get("score_home"), m.get("score_away")
    if sh is not None and sa is not None and sh != sa:
        win, lose = (h, a) if sh > sa else (a, h)
        info.update({"winner_key": win, "loser_key": lose,
                     # banter: a watched rival lost (to anyone); extra spicy if a favourite beat them
                     "banter": ROLE.get(lose) == "rival",
                     "banter_by_favourite": ROLE.get(lose) == "rival" and ROLE.get(win) == "favourite",
                     "favourite_lost": ROLE.get(lose) == "favourite"})
    return info


def day_matches(c, day, status):
    res = c.date.get(day.isoformat(), status=status)
    out = []
    for m in plain(res.matches):
        w = watched(m)
        if w:
            m.update(w)
            out.append(m)
    return out


def cmd_schedule(days):
    c = client()
    today = dt.date.today()
    fixtures = []
    for i in range(days + 1):
        d = today + dt.timedelta(days=i)
        fixtures += day_matches(c, d, "all")
    save(os.path.join(DATA, "fixtures.json"), {"generated": dt.datetime.utcnow().isoformat() + "Z", "fixtures": fixtures})
    fixtures.sort(key=lambda m: (not m["favourite_involved"], str(m.get("time_utc"))))
    for m in fixtures:
        print("*" if m["favourite_involved"] else " ", m.get("time_utc"), m["home_team"]["name"], "vs", m["away_team"]["name"], m.get("status"), m.get("id"))


def cmd_today():
    c = client()
    ms = day_matches(c, dt.date.today(), "all")
    ms.sort(key=lambda m: not m["favourite_involved"])   # favourites first
    save(os.path.join(DATA, "today.json"), {"date": dt.date.today().isoformat(), "matches": ms})
    for m in ms:
        tag = "BANTER" if m.get("banter") else ("FAV" if m["favourite_involved"] else "")
        print(f"{tag:6s}", m.get("id"), m.get("status"), m["home_team"]["name"], m.get("score_home"), "-", m.get("score_away"), m["away_team"]["name"], m.get("time_utc"))


ENDPOINTS = ["get", "lineups", "stats", "players", "events", "shots", "momentum",
             "advanced", "advanced_players", "advanced_network", "players_halves", "h2h"]


def cmd_fetch(mid):
    c = client()
    d = os.path.join(DATA, "matches", mid)
    os.makedirs(d, exist_ok=True)
    report = {}
    for ep in ENDPOINTS:
        try:
            res = getattr(c.matches, ep)(mid)
            save(os.path.join(d, f"{ep if ep != 'get' else 'match'}.json"), plain(res))
            report[ep] = "ok"
        except Exception as e:  # missing analytics on some leagues/plans is normal
            report[ep] = f"{type(e).__name__}: {getattr(e, 'code', '') or e}"
    save(os.path.join(d, "_fetch_report.json"), report)
    for k, v in report.items():
        print(f"{k:18s} {v}")


def save(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("schedule"); s.add_argument("--days", type=int, default=7)
    sub.add_parser("today")
    f = sub.add_parser("fetch"); f.add_argument("match_id")
    a = ap.parse_args()
    {"schedule": lambda: cmd_schedule(a.days), "today": cmd_today, "fetch": lambda: cmd_fetch(a.match_id)}[a.cmd]()
