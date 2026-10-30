"""24-hour performance review data for posted reels (the analysis itself is done by the performance-analyst agent).

  python3 engine/performance.py due                      -> reels posted 24 h+ ago that have no review yet (JSON)
  python3 engine/performance.py save <reel_id> <file>    -> data/performance/<reel_id>.json from a saved Zernio
                                                            analytics_get_analytics response (single post)
  python3 engine/performance.py table                    -> every reviewed reel: metrics, features, channel medians

Metrics come from Zernio (Instagram insights). Features come from the reel's own files (reel.json, timing.json,
caption.txt, insights.json, trends.json) so the agent can compare what was made with how it did.
"""
import ast, datetime as dt, json, os, re, statistics, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
PERF = os.path.join(DATA, "performance")
CFG = json.load(open(os.path.join(ROOT, "config/teams.json")))
NUM_WORDS = r"\b(zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred)\b"


def now():
    return dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)


def ts(s):
    """ISO time (any offset, 'Z' or none) -> naive UTC."""
    if not s:
        return None
    t = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    return t.astimezone(dt.timezone.utc).replace(tzinfo=None) if t.tzinfo else t


def load(path, default=None):
    try:
        return json.load(open(path))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def cmd_due():
    state = load(os.path.join(DATA, "state.json"), {"done": []})
    out = []
    for d in state.get("done", []):
        if not d.get("zernio_post"):
            continue
        t = ts(d.get("published_at") or d.get("scheduled_for"))
        if not t or now() - t < dt.timedelta(hours=24):
            continue
        if os.path.exists(os.path.join(PERF, f"{d['reel']}.review.md")):
            continue
        out.append({"reel": d["reel"], "zernio_post": d["zernio_post"], "posted": t.isoformat() + "Z",
                    "hours_since": round((now() - t).total_seconds() / 3600, 1)})
    print(json.dumps(out, indent=1))


def features(reel_id):
    rdir = os.path.join(ROOT, "reels", reel_id)
    reel = load(os.path.join(rdir, "reel.json"), {})
    timing = load(os.path.join(rdir, "timing.json"), {})
    match_dir = os.path.join(DATA, "matches", reel_id)
    ins = load(os.path.join(match_dir, "insights.json"), {})
    trends = load(os.path.join(match_dir, "trends.json"))
    beats = reel.get("beats", [])
    hook = beats[0] if beats else {}
    say0 = hook.get("say", "")
    tb = timing.get("beats", [])
    banter_i = next((i for i, b in enumerate(beats) if (b.get("card") or {}).get("type") == "banter"), None)
    caption = ""
    try:
        caption = open(os.path.join(rdir, "caption.txt")).read()
    except FileNotFoundError:
        pass
    m = ins.get("match", {})
    shorts = {m.get("home_short"), m.get("away_short")} - {None}
    favs = {t["key"] for t in CFG["teams"] if t.get("role") == "favourite"}
    rc = ins.get("result_context", {})
    return {
        "hook_say": say0,
        "hook_card": (hook.get("card") or {}).get("text", ""),
        "hook_emotion": hook.get("emotion"),
        "hook_words": len(say0.split()),
        "hook_seconds": round(tb[0]["end"] - tb[0]["start"], 2) if tb else None,
        "hook_has_number": bool(re.search(r"\d", say0) or re.search(NUM_WORDS, say0, re.I)),
        "hook_is_question": say0.strip().endswith("?"),
        "duration_s": timing.get("duration"),
        "beats": len(beats),
        "emotions": [b.get("emotion") for b in beats],
        "has_banter": banter_i is not None,
        "banter_at_s": tb[banter_i]["start"] if banter_i is not None and banter_i < len(tb) else None,
        "has_anger": any(b.get("emotion") in ("angry", "furious") for b in beats),
        "trend_used": reel.get("trend_used"),
        "trends_available": len((trends or {}).get("talking_points", [])) if trends else None,
        "league": (reel.get("match") or {}).get("league"),
        "pill": (reel.get("match") or {}).get("pill"),
        "favourite_involved": bool(shorts & favs) or any(t["key"] in favs and t["name"] in json.dumps(m) for t in CFG["teams"]),
        "result": "favourite_lost" if rc.get("favourite_lost") else "rival_lost_to_favourite" if rc.get("banter_by_favourite")
                  else "rival_lost" if rc.get("banter") else "other",
        "caption_first_line": caption.strip().split("\n")[0] if caption else "",
        "outro_question": next((b.get("say") for b in reversed(beats)
                                if (b.get("card") or {}).get("type") == "outro" or "?" in b.get("say", "")), None),
        "match_date": m.get("date"),
    }


def metrics(resp):
    a = resp.get("analytics", resp)
    dur = a.get("videoDurationSeconds")
    curve = a.get("retentionCurve") or None
    completion = a.get("completionRate")
    if completion == 0 and not curve:
        completion = None    # Instagram often sends 0 when it has no completion data
    watch = (a.get("igReelsAvgWatchTime") or 0) / 1000
    views = a.get("views") or 0
    reach = a.get("reach") or 0
    eng = sum((a.get(k) or 0) for k in ("likes", "comments", "shares", "saves"))
    return {
        "views": views, "reach": reach, "likes": a.get("likes"), "comments": a.get("comments"),
        "shares": a.get("shares"), "saves": a.get("saves"), "follows": a.get("follows"),
        "profile_views": a.get("profileViews"), "replays": a.get("replays"),
        "avg_watch_s": round(watch, 2), "video_s": dur,
        "watch_ratio": round(watch / dur, 3) if dur else None,
        "skip_rate": a.get("reelsSkipRate"), "completion_rate": completion,
        "total_watch_s": round((a.get("igReelsVideoViewTotalTime") or 0) / 1000, 1),
        "engagement_rate": a.get("engagementRate"),
        "engagements_per_1k_reach": round(eng * 1000 / reach, 1) if reach else None,
        "shares_saves_per_1k_reach": round(((a.get("shares") or 0) + (a.get("saves") or 0)) * 1000 / reach, 1) if reach else None,
        "retention_curve": curve,
        "url": a.get("platformPostUrl") or resp.get("platformPostUrl"),
        "last_updated": a.get("lastUpdated"),
    }


def cmd_save(reel_id, path):
    raw = open(path).read().strip()
    try:
        resp = json.loads(raw)
    except json.JSONDecodeError:
        resp = ast.literal_eval(raw)           # the MCP tool returns a Python-style dict string
    if isinstance(resp, dict) and isinstance(resp.get("result"), str):
        try:
            resp = json.loads(resp["result"])
        except json.JSONDecodeError:
            resp = ast.literal_eval(resp["result"])
    state = load(os.path.join(DATA, "state.json"), {"done": []})
    entry = next((d for d in state.get("done", []) if d.get("reel") == reel_id), {})
    posted = ts(resp.get("publishedAt") or entry.get("published_at") or entry.get("scheduled_for"))
    t = posted
    m = metrics(resp)
    upd = ts(m.get("last_updated"))
    feats = features(reel_id)
    md = feats.get("match_date")
    out = {"reel": reel_id, "zernio_post": resp.get("postId") or entry.get("zernio_post"),
           "posted_at": posted.isoformat() + "Z" if posted else None,
           "post_hour_utc": t.hour if t else None, "post_weekday": t.strftime("%a") if t else None,
           "snapshot_at": now().isoformat(timespec="seconds") + "Z",
           "hours_since_post": round((now() - posted).total_seconds() / 3600, 1) if posted else None,
           "data_age_h": round((upd - posted).total_seconds() / 3600, 1) if upd and posted else None,
           "hours_after_match": round((posted - dt.datetime.fromisoformat(md[:10])).total_seconds() / 3600) if posted and md and re.match(r"\d{4}-\d{2}-\d{2}", md) else None,
           "metrics": m, "features": feats}
    os.makedirs(PERF, exist_ok=True)
    json.dump(out, open(os.path.join(PERF, f"{reel_id}.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps({**out["metrics"], "data_age_h": out["data_age_h"], "hours_after_match": out["hours_after_match"]}, indent=1))


def cmd_table():
    rows = []
    for f in sorted(os.listdir(PERF)) if os.path.isdir(PERF) else []:
        if f.endswith(".json") and not f.startswith("_"):
            rows.append(load(os.path.join(PERF, f)))
    keys = ["views", "reach", "avg_watch_s", "watch_ratio", "skip_rate", "completion_rate", "engagements_per_1k_reach", "shares_saves_per_1k_reach", "follows"]
    med = {}
    for k in keys:
        vals = [r["metrics"][k] for r in rows if isinstance(r["metrics"].get(k), (int, float))]
        med[k] = statistics.median(vals) if vals else None
    print(json.dumps({"reels_reviewed": len(rows), "channel_median": med,
                      "reels": [{"reel": r["reel"], "posted_at": r["posted_at"], "hour_utc": r["post_hour_utc"], "weekday": r.get("post_weekday"),
                                 "data_age_h": r.get("data_age_h"), "hours_after_match": r.get("hours_after_match"),
                                 "metrics": {k: r["metrics"].get(k) for k in keys},
                                 "hook": r["features"]["hook_say"], "hook_emotion": r["features"]["hook_emotion"],
                                 "duration_s": r["features"]["duration_s"], "has_banter": r["features"]["has_banter"],
                                 "trend_used": r["features"]["trend_used"], "result": r["features"]["result"]}
                                for r in rows]}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "due":
        cmd_due()
    elif cmd == "save" and len(sys.argv) == 4:
        cmd_save(sys.argv[2], sys.argv[3])
    elif cmd == "table":
        cmd_table()
    else:
        sys.exit(__doc__)
