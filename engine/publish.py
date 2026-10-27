"""Upload a finished reel to Zernio storage and print its public URL.

  python3 engine/publish.py upload <uploadUrl> reels/<id>/out/reel.mp4

The presigned uploadUrl comes from Zernio's media_get_media_presigned_url tool
(the Publisher agent calls it). Needs the storage host (*.r2.cloudflarestorage.com)
allowed in the cloud environment's network settings.
"""
import sys, urllib.request


def upload(url, path):
    data = open(path, "rb").read()
    req = urllib.request.Request(url, data=data, method="PUT", headers={"Content-Type": "video/mp4"})
    with urllib.request.urlopen(req, timeout=300) as r:
        print("upload status", r.status, f"{len(data)/1e6:.1f} MB")


if __name__ == "__main__":
    if sys.argv[1] == "upload":
        upload(sys.argv[2], sys.argv[3])
