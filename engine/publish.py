"""Get a finished reel to Zernio.

  python3 engine/publish.py host <reel_id>
      Re-encodes reels/<id>/out/reel.mp4 for Instagram (H.264 Main 4.1, 30 fps, faststart),
      commits it to the `media` branch of the (public) GitHub repo and prints a commit-pinned
      raw.githubusercontent.com URL. Pass that URL to Zernio posts_create as media_urls.
      (Used because Zernio's own upload storage, *.r2.cloudflarestorage.com, is blocked here.)

  python3 engine/publish.py upload <presignedUploadUrl> <file>
      Direct upload to Zernio storage, once *.r2.cloudflarestorage.com is allowed.

  python3 engine/publish.py cleanup <reel_id>
      Removes a hosted video from the media branch after it has been published.
"""
import os, subprocess, sys, tempfile, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "compandgrow/thescoutsbrief"
GIT_ID = ["-c", "user.name=Scout Brief", "-c", "user.email=iamjazzys@proton.me"]


def sh(*cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def media_worktree():
    wt = os.path.join(tempfile.gettempdir(), "scout-media-wt")
    if not os.path.isdir(wt):
        sh("git", "fetch", "-q", "origin", "media", cwd=ROOT)
        sh("git", "worktree", "add", "-q", "-B", "media", wt, "origin/media", cwd=ROOT)
    else:
        sh("git", "pull", "-q", "origin", "media", cwd=wt)
    return wt


def host(reel_id):
    src = os.path.join(ROOT, "reels", reel_id, "out", "reel.mp4")
    ig = os.path.join(ROOT, "reels", reel_id, "out", "reel_instagram.mp4")
    sh("ffmpeg", "-y", "-loglevel", "error", "-i", src, "-c:v", "libx264", "-profile:v", "main", "-level:v", "4.1",
       "-pix_fmt", "yuv420p", "-r", "30", "-crf", "19", "-preset", "medium", "-c:a", "aac", "-b:a", "160k",
       "-ar", "44100", "-movflags", "+faststart", ig)
    wt = media_worktree()
    os.makedirs(os.path.join(wt, "reels"), exist_ok=True)
    dst = os.path.join(wt, "reels", f"{reel_id}.mp4")
    with open(ig, "rb") as a, open(dst, "wb") as b:
        b.write(a.read())
    sh("git", "add", "-A", cwd=wt)
    sh("git", *GIT_ID, "commit", "-q", "-m", f"Host reel video: {reel_id}", cwd=wt)
    sh("git", "push", "-q", "origin", "media", cwd=wt)
    sha = sh("git", "rev-parse", "HEAD", cwd=wt)
    print(f"https://raw.githubusercontent.com/{REPO}/{sha}/reels/{reel_id}.mp4")


def cleanup(reel_id):
    wt = media_worktree()
    p = os.path.join(wt, "reels", f"{reel_id}.mp4")
    if os.path.exists(p):
        sh("git", "rm", "-q", p, cwd=wt)
        sh("git", *GIT_ID, "commit", "-q", "-m", f"Remove hosted video after posting: {reel_id}", cwd=wt)
        sh("git", "push", "-q", "origin", "media", cwd=wt)
        print("removed", reel_id)


def upload(url, path):
    data = open(path, "rb").read()
    req = urllib.request.Request(url, data=data, method="PUT", headers={"Content-Type": "video/mp4"})
    with urllib.request.urlopen(req, timeout=300) as r:
        print("upload status", r.status, f"{len(data)/1e6:.1f} MB")


if __name__ == "__main__":
    cmd = sys.argv[1]
    {"host": lambda: host(sys.argv[2]), "cleanup": lambda: cleanup(sys.argv[2]),
     "upload": lambda: upload(sys.argv[2], sys.argv[3])}[cmd]()
