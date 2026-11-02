"""Fan buzz from Reddit through the official API (app-only OAuth, read-only).

Two modes, picked automatically:
- API (best: upvotes and comment counts): REDDIT_CLIENT_ID + REDDIT_CLIENT_SECRET (a free "script" app at
  reddit.com/prefs/apps), with www.reddit.com + oauth.reddit.com allowed.
- RSS (no keys): Reddit's public feeds, with only www.reddit.com allowed. Same posts in Reddit's own "hot" order,
  but no upvote/comment counts, so heat is the feed rank. Force it with REDDIT_MODE=rss.

  python3 engine/reddit.py trending [--sub soccer] [--limit 25]   -> hottest posts now (topics fans are on)
  python3 engine/reddit.py match "<home>" "<away>" [--days 2]     -> r/soccer (post-)match thread + top comments
  python3 engine/reddit.py club <KEY> [--limit 15]                -> hot posts in a watched club's subreddit
  python3 engine/reddit.py digest                                  -> data/trends/<date>.json: r/soccer + every club sub

Rules built in:
- Read-only. Nothing is posted, voted or messaged.
- Usernames are never stored. Comment text is kept short, for theme-spotting only.
- Reddit is a signal of what fans talk about, never a source of facts: a claim from Reddit must be confirmed by a
  trusted site (research.trusted_domains) before it goes on screen.
- Results are cached in data/reddit/ with fetch time; the same request within 20 minutes reuses the cache.
"""
import argparse, base64, html, xml.etree.ElementTree as ET, datetime as dt, hashlib, json, os, re, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "config/teams.json")))
RCFG = CFG.get("reddit", {})
CACHE = os.path.join(ROOT, "data/reddit")
TOKEN = os.path.join(CACHE, ".token.json")
UA = RCFG.get("user_agent", "linux:thescoutbrief-trends:v1.0 (read-only fan-trend research)")


MODE = os.environ.get("REDDIT_MODE") or ("api" if os.environ.get("REDDIT_CLIENT_ID") and os.environ.get("REDDIT_CLIENT_SECRET") else "rss")
ATOM = {"a": "http://www.w3.org/2005/Atom"}
RSS_GAP_S = 8          # keyless feeds allow ~10 requests/minute
_last = [0.0]


class RedditError(Exception):
    pass


def now():
    return dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)


def token():
    try:
        t = json.load(open(TOKEN))
        if t["expires"] > time.time() + 60:
            return t["access_token"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        pass
    cid, sec = os.environ.get("REDDIT_CLIENT_ID"), os.environ.get("REDDIT_CLIENT_SECRET")
    if not cid or not sec:
        sys.exit("REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET are not set (add them to the environment's variables)")
    req = urllib.request.Request("https://www.reddit.com/api/v1/access_token", method="POST",
                                 data=b"grant_type=client_credentials",
                                 headers={"Authorization": "Basic " + base64.b64encode(f"{cid}:{sec}".encode()).decode(),
                                          "User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Reddit token error {e.code}: {e.read()[:300].decode(errors='replace')}")
    except urllib.error.URLError as e:
        sys.exit(f"Cannot reach www.reddit.com ({e.reason}); is it in the allowed domains?")
    if "access_token" not in d:
        sys.exit(f"Reddit token error: {d}")
    os.makedirs(CACHE, exist_ok=True)
    json.dump({"access_token": d["access_token"], "expires": time.time() + d.get("expires_in", 3600)}, open(TOKEN, "w"))
    os.chmod(TOKEN, 0o600)
    return d["access_token"]


def get(path, params=None, max_age_min=20):
    url = f"https://oauth.reddit.com{path}?" + urllib.parse.urlencode({**(params or {}), "raw_json": 1})
    key = hashlib.sha1(url.encode()).hexdigest()[:12]
    cpath = os.path.join(CACHE, f"{key}.json")
    try:
        c = json.load(open(cpath))
        if (now() - dt.datetime.fromisoformat(c["fetched_at"].rstrip("Z"))).total_seconds() < max_age_min * 60:
            return c["data"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        pass
    for attempt in range(3):
        req = urllib.request.Request(url, headers={"Authorization": f"bearer {token()}", "User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
                left = r.headers.get("x-ratelimit-remaining")
                if left and float(left) < 5:
                    time.sleep(float(r.headers.get("x-ratelimit-reset", 10)))
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(15)
                continue
            if e.code == 401 and attempt < 2:
                os.remove(TOKEN) if os.path.exists(TOKEN) else None
                continue
            sys.exit(f"Reddit error {e.code} on {path}: {e.read()[:200].decode(errors='replace')}")
        except urllib.error.URLError as e:
            sys.exit(f"Cannot reach oauth.reddit.com ({e.reason}); is it in the allowed domains?")
    os.makedirs(CACHE, exist_ok=True)
    json.dump({"url": url, "fetched_at": now().isoformat(timespec="seconds") + "Z", "data": data}, open(cpath, "w"))
    return data


def get_rss(path, params=None, max_age_min=20):
    """Public Atom feed -> list of entries (no keys needed)."""
    url = f"https://www.reddit.com{path}.rss?" + urllib.parse.urlencode(params or {})
    key = hashlib.sha1(url.encode()).hexdigest()[:12]
    cpath = os.path.join(CACHE, f"rss_{key}.json")
    try:
        c = json.load(open(cpath))
        if (now() - dt.datetime.fromisoformat(c["fetched_at"].rstrip("Z"))).total_seconds() < max_age_min * 60:
            return c["data"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        pass
    for attempt in range(4):
        wait = RSS_GAP_S - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r:
                root = ET.fromstring(r.read())
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                ra = e.headers.get("Retry-After")
                time.sleep(int(ra) + 2 if ra and ra.isdigit() else 30 * (attempt + 1))
                continue
            raise RedditError(f"Reddit RSS error {e.code} on {path}" + (" (Reddit is blocking unauthenticated requests: use the API keys)" if e.code == 403 else ""))
        except urllib.error.URLError as e:
            raise RedditError(f"Cannot reach www.reddit.com ({e.reason}); is it in the allowed domains?")
    data = []
    for e in root.findall("a:entry", ATOM):
        link = (e.find("a:link", ATOM).get("href") if e.find("a:link", ATOM) is not None else "")
        cat = e.find("a:category", ATOM)
        body = e.findtext("a:content", "", ATOM)
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", html.unescape(body)))).strip()
        data.append({"id": (e.findtext("a:id", "", ATOM) or "").split("_")[-1], "title": e.findtext("a:title", "", ATOM),
                     "link": link, "time": e.findtext("a:published", None, ATOM) or e.findtext("a:updated", "", ATOM),
                     "subreddit": cat.get("term") if cat is not None else None, "text": text})
    os.makedirs(CACHE, exist_ok=True)
    json.dump({"url": url, "fetched_at": now().isoformat(timespec="seconds") + "Z", "data": data}, open(cpath, "w"))
    return data


PINNED = re.compile(r"(daily|weekly|monthly)\b.*\b(discussion|thread)|open thread|\bAMA\b|transfer thread|free talk|megathread|moan thread|discussion thread", re.I)


def rss_row(e, rank, total):
    try:
        t = dt.datetime.fromisoformat(e["time"].replace("Z", "+00:00")).astimezone(dt.timezone.utc).replace(tzinfo=None)
        age_h = round((now() - t).total_seconds() / 3600, 1)
    except (ValueError, AttributeError):
        age_h = None
    m = re.search(r"/comments/([a-z0-9]+)/", e["link"])
    return {"title": e["title"], "flair": None, "score": None, "comments": None, "upvote_ratio": None, "age_h": age_h,
            "heat": total - rank, "rank": rank + 1, "domain": None, "link": e["link"], "permalink": e["link"],
            "id": m.group(1) if m else e["id"], "subreddit": e.get("subreddit"), "source": "rss (Reddit hot order; no counts)"}


def post_row(p):
    d = p["data"]
    age_h = (time.time() - d["created_utc"]) / 3600
    return {"title": d["title"], "flair": d.get("link_flair_text"), "score": d["score"],
            "comments": d["num_comments"], "upvote_ratio": d.get("upvote_ratio"),
            "age_h": round(age_h, 1), "heat": round((d["score"] + 2 * d["num_comments"]) / max(age_h, 1), 1),
            "domain": d.get("domain"), "link": d.get("url_overridden_by_dest") or d.get("url"),
            "permalink": "https://www.reddit.com" + d["permalink"], "id": d["id"], "subreddit": d["subreddit"]}


def listing(sub, kind="hot", limit=25, t=None):
    if MODE == "rss":
        es = get_rss(f"/r/{sub}/{kind}/", {"limit": limit, **({"t": t} if t else {})})
        es = [e for e in es if not PINNED.search(e["title"])]       # feeds include pinned threads; drop them
        return [rss_row(e, i, len(es)) for i, e in enumerate(es)]
    params = {"limit": limit}
    if t:
        params["t"] = t
    data = get(f"/r/{sub}/{kind}", params)
    return [post_row(p) for p in data["data"]["children"] if not p["data"].get("stickied") and not p["data"].get("over_18")]


def top_comments(post_id, n=12):
    if MODE == "rss":
        es = get_rss(f"/comments/{post_id}/", {"sort": "top", "limit": n})
        return [{"score": None, "text": e["text"][:220]} for e in es[1:] if e["text"] and e["text"] not in ("[deleted]", "[removed]")][:n]
    data = get(f"/comments/{post_id}", {"sort": "top", "limit": n, "depth": 1})
    out = []
    for c in data[1]["data"]["children"]:
        if c["kind"] != "t1":
            continue
        body = re.sub(r"\s+", " ", c["data"].get("body", "")).strip()
        if body in ("[deleted]", "[removed]") or not body:
            continue
        out.append({"score": c["data"]["score"], "text": body[:220]})   # no usernames
    return out


def cmd_trending(sub, limit):
    rows = sorted(listing(sub, "hot", limit), key=lambda r: -r["heat"])
    print(json.dumps({"subreddit": sub, "mode": MODE, "fetched_at": now().isoformat(timespec="seconds") + "Z", "posts": rows}, indent=1, ensure_ascii=False))


def names_for(team):
    for t in CFG["teams"]:
        if team.lower() in [t["name"].lower(), t["key"].lower()] + [a.lower() for a in t.get("aliases", [])]:
            return [t["name"]] + t.get("aliases", [])
    return [team]


def cmd_match(home, away, days):
    hn, an = names_for(home), names_for(away)
    found = []
    for q in (f'flair:"Post Match Thread" {home}', f'"Match Thread" {home} {away}', f"{home} {away}"):
        if MODE == "rss":
            es = get_rss("/r/soccer/search", {"q": q, "restrict_sr": 1, "sort": "new", "t": "week", "limit": 15})
            rows = [rss_row(e, i, len(es)) for i, e in enumerate(es)]
        else:
            rows = [post_row(p) for p in get("/r/soccer/search", {"q": q, "restrict_sr": 1, "sort": "new", "t": "week", "limit": 15})["data"]["children"]]
        for r in rows:
            title = r["title"].lower()
            if (r["age_h"] or 0) > days * 24 or r["id"] in {f["id"] for f in found}:
                continue
            if any(n.lower() in title for n in hn) and any(n.lower() in title for n in an):
                found.append(r)
    found.sort(key=lambda r: (0 if "post match" in r["title"].lower() else 1 if "match thread" in r["title"].lower() else 2, -(r["comments"] or 0)))
    out = {"match": f"{home} v {away}", "mode": MODE, "fetched_at": now().isoformat(timespec="seconds") + "Z", "threads": found[:6]}
    if found:
        out["top_comments"] = top_comments(found[0]["id"])
        out["comments_from"] = found[0]["permalink"]
    print(json.dumps(out, indent=1, ensure_ascii=False))


def cmd_club(key, limit):
    t = next((t for t in CFG["teams"] if t["key"] == key.upper()), None)
    sub = (t or {}).get("subreddit")
    if not sub:
        sys.exit(f"No subreddit for {key} in config/teams.json")
    rows = sorted(listing(sub, "hot", limit), key=lambda r: -r["heat"])
    print(json.dumps({"club": key.upper(), "subreddit": sub, "posts": rows}, indent=1, ensure_ascii=False))


def cmd_digest():
    out = {"date": dt.date.today().isoformat(), "mode": MODE, "fetched_at": now().isoformat(timespec="seconds") + "Z",
           "soccer": sorted(listing("soccer", "hot", 40), key=lambda r: -r["heat"])[:20], "clubs": {}}
    out["errors"] = {}
    for t in CFG["teams"]:
        if t.get("subreddit"):
            try:
                out["clubs"][t["key"]] = sorted(listing(t["subreddit"], "hot", 15), key=lambda r: -r["heat"])[:6]
            except RedditError as e:
                out["errors"][t["key"]] = str(e)
    os.makedirs(os.path.join(ROOT, "data/trends"), exist_ok=True)
    path = os.path.join(ROOT, "data/trends", f"{out['date']}.json")
    json.dump(out, open(path, "w"), indent=1, ensure_ascii=False)
    print(f"saved {path}")
    for r in out["soccer"][:12]:
        counts = f"{r['score']:6d}↑ {r['comments']:5d}💬" if r["score"] is not None else f"#{r.get('rank', '?'):<3} (rss)  "
        print(f"  heat {r['heat']:7.1f}  {counts}  [{r['flair'] or '-'}] {r['title'][:90]}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("trending"); s.add_argument("--sub", default="soccer"); s.add_argument("--limit", type=int, default=25)
    m = sub.add_parser("match"); m.add_argument("home"); m.add_argument("away"); m.add_argument("--days", type=int, default=2)
    c = sub.add_parser("club"); c.add_argument("key"); c.add_argument("--limit", type=int, default=15)
    sub.add_parser("digest")
    a = ap.parse_args()
    {"trending": lambda: cmd_trending(a.sub, a.limit), "match": lambda: cmd_match(a.home, a.away, a.days),
     "club": lambda: cmd_club(a.key, a.limit), "digest": cmd_digest}[a.cmd]()


if __name__ == "__main__":
    try:
        main()
    except RedditError as e:
        sys.exit(str(e))
