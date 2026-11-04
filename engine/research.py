"""Web research for the agents: free local fetching (Scrapling) first, Firecrawl as the fallback.

scrape: fetches trusted pages directly with Scrapling's plain HTTP fetcher (free, no credits) when the site is
in the environment's allowed domains; falls back to Firecrawl if the local fetch fails or returns too little.
search: always Firecrawl (it needs a search engine).
Needs: scrapling[fetchers] (setup.sh) and the trusted sites allowed; FIRECRAWL_API_KEY + api.firecrawl.dev for
the fallback and for search.

  python3 engine/research.py search "Arsenal injury news" [--limit 5] [--days 3] [--site bbc.co.uk]
  python3 engine/research.py scrape https://www.bbc.co.uk/sport/football/...
  python3 engine/research.py usage

Rules built in:
- Only domains in config/teams.json -> research.trusted_domains (search is filtered to them,
  scrape refuses others). Stats sites that forbid scraping are not on the list.
- Every result is cached in data/research/ with its URL and fetch time, so a fact can cite it.
- A monthly credit budget stops runs before the free tier (1,000/month) is used up.
"""
import argparse, datetime as dt, hashlib, json, os, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "config/teams.json"))).get("research", {})
DIR = os.path.join(ROOT, "data/research")
USAGE = os.path.join(DIR, "usage.json")
API = "https://api.firecrawl.dev/v2"
TRUSTED = CFG.get("trusted_domains", [])
BUDGET = CFG.get("monthly_credit_budget", 800)
COST = {"scrape": 1, "search_result": 1}   # estimate when the API doesn't report credits
LOCAL_FIRST = CFG.get("local_fetch", {}).get("enabled", True)
LOCAL_SKIP = set(CFG.get("local_fetch", {}).get("firecrawl_only_domains", []))
LOCAL_MUST = CFG.get("local_fetch", {}).get("must_contain", {})   # url part -> text a complete page must contain
LOCAL_MIN_CHARS = 1500
_last_local = {}


def month():
    return dt.date.today().strftime("%Y-%m")


def usage():
    try:
        u = json.load(open(USAGE))
    except (FileNotFoundError, json.JSONDecodeError):
        u = {}
    return u


def spend(n, what):
    u = usage()
    m = u.setdefault(month(), {"credits": 0, "calls": []})
    m["credits"] += n
    m["calls"].append({"at": dt.datetime.now(dt.timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds") + "Z", "what": what, "credits": n})
    os.makedirs(DIR, exist_ok=True)
    json.dump(u, open(USAGE, "w"), indent=1)


def check_budget(need):
    used = usage().get(month(), {}).get("credits", 0)
    if used + need > BUDGET:
        sys.exit(f"Research budget reached: {used}/{BUDGET} credits used this month. Skipping web research.")


def trusted(url):
    host = urllib.parse.urlparse(url).hostname or ""
    return any(host == d or host.endswith("." + d) for d in TRUSTED)


def call(path, body):
    key = os.environ.get("FIRECRAWL_API_KEY")
    if not key:
        sys.exit("FIRECRAWL_API_KEY is not set (add it to the environment's variables)")
    req = urllib.request.Request(f"{API}/{path}", data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    import time
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read()[:400].decode(errors="replace")
            if e.code == 429 and attempt < 3:      # free plan: ~10 requests/minute
                wait = 35
                try:
                    wait = int(json.loads(body).get("retry_after_seconds", 35)) + 2
                except Exception:
                    pass
                print(f"rate limited, waiting {wait}s", file=sys.stderr)
                time.sleep(wait)
                req = urllib.request.Request(req.full_url, data=req.data, method="POST", headers=dict(req.header_items()))
                continue
            sys.exit(f"Firecrawl error {e.code}: {body[:300]}")
        except urllib.error.URLError as e:
            sys.exit(f"Cannot reach api.firecrawl.dev ({e.reason}); is it in the allowed domains?")
    sys.exit("Firecrawl: still rate limited after retries")


def cache(kind, key, data):
    os.makedirs(DIR, exist_ok=True)
    name = f"{kind}_{hashlib.sha1(key.encode()).hexdigest()[:12]}.json"
    path = os.path.join(DIR, name)
    json.dump({"kind": kind, "key": key, "fetched_at": dt.datetime.now(dt.timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds") + "Z", "data": data},
              open(path, "w"), indent=1, ensure_ascii=False)
    return path


def credits_from(resp, fallback):
    for k in ("creditsUsed", "credits_used"):
        if isinstance(resp.get(k), (int, float)):
            return int(resp[k])
    return fallback


def local_fetch(url):
    """Plain HTTP fetch with Scrapling (no browser, no anti-bot tricks) -> markdown, or None to fall back."""
    host = urllib.parse.urlparse(url).hostname or ""
    if not LOCAL_FIRST or any(host == d or host.endswith("." + d) for d in LOCAL_SKIP):
        return None
    try:
        import logging, re, time
        from scrapling.fetchers import Fetcher
        from scrapling.core.shell import Convertor
        logging.getLogger("scrapling").setLevel(logging.WARNING)     # keep stdout clean (agents parse "saved <path>")
        from markdownify import markdownify
        wait = 1.5 - (time.time() - _last_local.get(host, 0))     # be polite: max ~1 request/1.5 s per site
        if wait > 0:
            time.sleep(wait)
        _last_local[host] = time.time()
        page = Fetcher.get(url, timeout=30)
        if page.status != 200:
            print(f"local fetch {page.status} for {url}, using Firecrawl", file=sys.stderr)
            return None
        body = page.css("body").first or page
        clean = Convertor._sanitize_for_ai(Convertor._strip_noise_tags(body))   # drop scripts + hidden prompt-injection text
        md = markdownify(clean.html_content, heading_style="ATX")
        base = f"{urllib.parse.urlparse(url).scheme}://{host}"
        md = re.sub(r"\]\((/[^)\s]*)", lambda m: "](" + base + m.group(1), md)   # absolute links, like Firecrawl
        md = re.sub(r"\n{3,}", "\n\n", md)
        title = page.css("title::text").get() if hasattr(page.css("title::text"), "get") else None
        missing = [w for part, words in LOCAL_MUST.items() if part in url for w in words if w not in md]
        if missing:
            print(f"local fetch lacks {missing} (loaded by JavaScript) for {url}, using Firecrawl", file=sys.stderr)
            return None
        if len(md) < LOCAL_MIN_CHARS:
            print(f"local fetch too short ({len(md)} chars) for {url}, using Firecrawl", file=sys.stderr)
            return None
        return {"markdown": md, "title": str(title) if title else None}
    except Exception as e:   # not installed, blocked by network policy, timeout, parse error
        print(f"local fetch failed for {url} ({type(e).__name__}: {str(e)[:120]}), using Firecrawl", file=sys.stderr)
        return None


def cmd_scrape(url):
    if not trusted(url):
        sys.exit(f"Refused: {urllib.parse.urlparse(url).hostname} is not in research.trusted_domains")
    loc = local_fetch(url)
    if loc:
        spend(0, f"local scrape {url}")
        path = cache("scrape", url, {"url": url, "title": loc["title"], "markdown": loc["markdown"], "via": "scrapling"})
        print(f"saved {path}\n")
        print(loc["markdown"][:6000])
        return
    check_budget(COST["scrape"])
    resp = call("scrape", {"url": url, "formats": ["markdown"], "onlyMainContent": True})
    spend(credits_from(resp, COST["scrape"]), f"scrape {url}")
    d = resp.get("data", resp)
    path = cache("scrape", url, {"url": url, "title": (d.get("metadata") or {}).get("title"), "markdown": d.get("markdown", ""), "via": "firecrawl"})
    print(f"saved {path}\n")
    print((d.get("markdown") or "")[:6000])


def cmd_search(query, limit, days, site=None):
    check_budget(limit * COST["search_result"])
    if site and not trusted("https://" + site):
        sys.exit(f"Refused: {site} is not in research.trusted_domains")
    body = {"query": query, "limit": limit, "includeDomains": [site] if site else TRUSTED}
    if days:
        body["tbs"] = f"qdr:{'d' if days == 1 else 'w' if days <= 7 else 'm'}"
    resp = call("search", body)
    spend(credits_from(resp, limit * COST["search_result"]), f"search {query}")
    d = resp.get("data", resp)
    items = d.get("web", d) if isinstance(d, dict) else d
    items = [i for i in (items or []) if trusted(i.get("url", ""))]
    path = cache("search", query, items)
    print(f"saved {path}")
    for i in items:
        print(f"- {i.get('title')}\n  {i.get('url')}\n  {(i.get('description') or '')[:200]}")


def cmd_usage():
    m = usage().get(month(), {"credits": 0, "calls": []})
    free = sum(1 for c in m["calls"] if c["what"].startswith("local scrape"))
    print(f"{month()}: {m['credits']}/{BUDGET} Firecrawl credits, {len(m['calls']) - free} Firecrawl calls, {free} free local fetches")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("query"); s.add_argument("--limit", type=int, default=5); s.add_argument("--days", type=int, default=0); s.add_argument("--site", help="search one trusted site only, e.g. kicker.de")
    c = sub.add_parser("scrape"); c.add_argument("url")
    sub.add_parser("usage")
    a = ap.parse_args()
    {"search": lambda: cmd_search(a.query, a.limit, a.days, a.site), "scrape": lambda: cmd_scrape(a.url), "usage": cmd_usage}[a.cmd]()
