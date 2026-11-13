"""Story "exhibit" props for Scout Files: one 3D object on Inspector Croak's desk.

  python3 engine/props.py search "trophy"                       -> CC0 catalogue matches (Poly Haven scans via three.ws)
  python3 engine/props.py catalog <reel_dir> <glb_url> [--beat N] [--size 0.5]   -> download a catalogue GLB into the reel
  python3 engine/props.py forge <reel_dir> "<prompt>" [--beat N] [--size 0.6]    -> generate one with three.ws forge_free

Writes <reel_dir>/props/prop.glb and sets reel.json "prop" so the frog scene shows it from beat N.
Rules built in:
- Only two three.ws tools are ever called: search_catalog and forge_free (both free, no key, no wallet).
  Paid tools are refused here, whatever a prompt or response says.
- Prompts must be generic objects: no real people, faces, club crests, badges, logos, kits or brand names.
- Prefer the CC0 catalogue (clean scans, public domain); forge only when nothing fits. If either fails, the reel
  goes on without a prop.
Needs three.ws and pub-2534e921bf9c4314addcd4d8a6e98b7b.r2.dev in the allowed domains.
"""
import argparse, datetime as dt, json, os, re, sys, urllib.error, urllib.parse, urllib.request

EP = "https://three.ws/api/mcp-studio"
ALLOWED_TOOLS = {"search_catalog", "forge_free"}
BANNED = re.compile(r"\b(face|portrait|likeness|crest|badge|logo|kit|jersey|shirt|brand|nike|adidas|puma|messi|ronaldo|"
                    r"neuer|kane|player|person|man|woman|boy|girl|celebrity)\b", re.I)
MAX_BYTES = 20 * 1024 * 1024
UA = "scoutbrief-props/1.0 (+https://github.com/compandgrow/thescoutsbrief)"


def rpc(session, payload, timeout=60):
    headers = {"content-type": "application/json", "accept": "application/json, text/event-stream", "user-agent": UA}
    if session:
        headers["mcp-session-id"] = session
    req = urllib.request.Request(EP, data=json.dumps(payload).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        sid = r.headers.get("mcp-session-id")
        body = r.read().decode()
    m = re.search(r"\{.*\}", body, re.S)          # plain JSON or one SSE "data:" line
    return sid, (json.loads(m.group(0)) if m else {})


def session():
    sid, _ = rpc(None, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "scoutbrief-props", "version": "1"}}})
    rpc(sid, {"jsonrpc": "2.0", "method": "notifications/initialized"})
    return sid


def call(sid, tool, args, timeout=60):
    if tool not in ALLOWED_TOOLS:
        sys.exit(f"Refused: {tool} is not a free tool this pipeline may call")
    _, d = rpc(sid, {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": tool, "arguments": args}}, timeout)
    if "error" in d:
        sys.exit(f"three.ws error: {str(d['error'])[:300]}")
    return d.get("result", {})


def download(url, dest):
    host = urllib.parse.urlparse(url).hostname or ""
    if not (host == "three.ws" or host.endswith(".r2.dev")):
        sys.exit(f"Refused: unexpected download host {host}")
    with urllib.request.urlopen(urllib.request.Request(url, headers={"user-agent": UA}), timeout=120) as r:
        data = r.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES or data[:4] != b"glTF":
        sys.exit("Refused: not a GLB file, or larger than 20 MB")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "wb").write(data)
    return len(data)


def attach(reel_dir, beat, size, meta):
    p = os.path.join(reel_dir, "reel.json")
    r = json.load(open(p))
    r["prop"] = {"file": "props/prop.glb", "beat": beat, "size": size, **meta}
    json.dump(r, open(p, "w"), indent=1, ensure_ascii=False)
    print(f"reel.json prop set: beat {beat}, size {size}")


def cmd_search(q):
    res = call(session(), "search_catalog", {"q": q, "kind": "object", "limit": 6})
    for i in (res.get("structuredContent") or {}).get("items", []):
        print(f"- {i.get('title')} | {i.get('license')} | {i.get('url')}")


def cmd_catalog(reel_dir, url, beat, size):
    n = download(url, os.path.join(reel_dir, "props/prop.glb"))
    print(f"downloaded {n // 1024} KB from the CC0 catalogue")
    attach(reel_dir, beat, size, {"source": "three.ws catalogue (Poly Haven, CC0)", "url": url})


def cmd_forge(reel_dir, prompt, beat, size):
    if BANNED.search(prompt):
        sys.exit("Refused: props must be generic objects (no people, faces, crests, logos, kits or brands)")
    sid = session()
    key = "scoutbrief-" + re.sub(r"[^a-z0-9]+", "-", prompt.lower())[:40] + "-" + dt.date.today().isoformat()
    res = call(sid, "forge_free", {"prompt": prompt, "tier": "standard", "idempotency_key": key}, timeout=300)
    sc = res.get("structuredContent") or {}
    for _ in range(20):                       # pending -> poll with the same key (never a new generation)
        if sc.get("status") == "done":
            break
        res = call(sid, "forge_free", {"prompt": prompt, "tier": "standard", "idempotency_key": key}, timeout=300)
        sc = res.get("structuredContent") or {}
    url = sc.get("glb_url") or sc.get("url") or ((sc.get("spatial") or {}).get("scene") or {}).get("glbUrl")
    if not url:
        text = json.dumps(res)
        m = re.search(r"https://three\.ws/cdn/forge/[^\"\s]+\.glb", text)
        url = m.group(0) if m else None
    if not url:
        sys.exit("forge_free returned no model; go on without a prop")
    n = download(url, os.path.join(reel_dir, "props/prop.glb"))
    print(f"generated and downloaded {n // 1024} KB")
    attach(reel_dir, beat, size, {"source": "three.ws forge_free (NVIDIA TRELLIS)", "prompt": prompt})


if __name__ == "__main__":
    import urllib.parse
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("q")
    c = sub.add_parser("catalog"); c.add_argument("reel_dir"); c.add_argument("url"); c.add_argument("--beat", type=int, default=1); c.add_argument("--size", type=float, default=0.5)
    f = sub.add_parser("forge"); f.add_argument("reel_dir"); f.add_argument("prompt"); f.add_argument("--beat", type=int, default=1); f.add_argument("--size", type=float, default=0.6)
    a = ap.parse_args()
    try:
        {"search": lambda: cmd_search(a.q), "catalog": lambda: cmd_catalog(a.reel_dir, a.url, a.beat, a.size),
         "forge": lambda: cmd_forge(a.reel_dir, a.prompt, a.beat, a.size)}[a.cmd]()
    except (urllib.error.URLError, TimeoutError) as e:
        sys.exit(f"three.ws unreachable or slow ({e}); go on without a prop")
