"""Voice the script offline with Kokoro and build the lip-sync track.

usage: python3 engine/voice.py reels/<id>/reel.json

Writes next to reel.json:
  audio/voice.wav   full narration on one timeline
  timing.json       start/end seconds per beat
  mouth.json        mouth openness 0..1 per frame (FPS below)
"""
import json, sys, os, subprocess
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

FPS = 30
SR = 24000
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Kokoro has no emotion control, so emotion is carried by pace and loudness.
STYLE = {
    "neutral":      {"speed": 1.05, "gain": 1.0},
    "smug":         {"speed": 1.00, "gain": 1.0},
    "happy":        {"speed": 1.10, "gain": 1.1},
    "excited":      {"speed": 1.15, "gain": 1.2},
    "shocked":      {"speed": 1.08, "gain": 1.15},
    "disappointed": {"speed": 0.94, "gain": 0.9},
    "laughing":     {"speed": 1.12, "gain": 1.2},
    "angry":        {"speed": 1.16, "gain": 1.35},
    "furious":      {"speed": 1.20, "gain": 1.5},
}
LEAD_IN = 0.45   # silence before first line
GAP = 0.40       # silence between lines
TAIL = 0.9       # silence after the last line


def main(path):
    reel = json.load(open(path))
    out_dir = os.path.dirname(os.path.abspath(path))
    os.makedirs(os.path.join(out_dir, "audio"), exist_ok=True)
    k = Kokoro(os.path.join(ROOT, "models/kokoro-v1.0.onnx"),
               os.path.join(ROOT, "models/voices-v1.0.bin"))
    cfg = json.load(open(os.path.join(ROOT, "config/teams.json"))).get("voice", {})
    voice = reel.get("voice", cfg.get("name", "am_onyx"))
    fx = {**cfg, **reel.get("voice_fx", {})}

    pieces, timing, t = [], [], LEAD_IN
    pieces.append(np.zeros(int(LEAD_IN * SR), np.float32))
    for i, beat in enumerate(reel["beats"]):
        st = STYLE.get(beat.get("emotion", "neutral"), STYLE["neutral"])
        speed = beat.get("speed", st["speed"])
        audio, sr = k.create(beat["say"], voice=voice, speed=speed, lang="en-us")
        assert sr == SR
        audio = trim(audio) * st["gain"]
        dur = len(audio) / SR
        timing.append({"beat": i, "start": round(t, 3), "end": round(t + dur, 3)})
        pieces.append(audio.astype(np.float32))
        gap = beat.get("pause_after", GAP)
        pieces.append(np.zeros(int(gap * SR), np.float32))
        t += dur + gap
        print(f"beat {i:2d} {beat.get('emotion','neutral'):12s} {dur:5.2f}s  {beat['say'][:60]}")
    pieces.append(np.zeros(int(TAIL * SR), np.float32))
    full = np.concatenate(pieces)
    peak = np.abs(full).max()
    if peak > 0.98:
        full = full * (0.98 / peak)
    raw = os.path.join(out_dir, "audio/voice_raw.wav")
    sf.write(raw, full, SR)
    full = apply_fx(raw, os.path.join(out_dir, "audio/voice.wav"), fx, len(full))

    total = len(full) / SR
    json.dump({"duration": round(total, 3), "beats": timing},
              open(os.path.join(out_dir, "timing.json"), "w"), indent=1)
    json.dump(mouth_track(full), open(os.path.join(out_dir, "mouth.json"), "w"))
    print(f"total {total:.2f}s")


def apply_fx(src, dst, fx, n):
    """Bolder gorilla voice: pitch down (formants follow, so it sounds bigger), bass, presence, compression."""
    semi = fx.get("pitch", -3)
    chain = [f"rubberband=pitch={2 ** (semi / 12):.5f}:formant=shifted" if semi else None,
             f"bass=g={fx.get('bass', 6)}:f=110",
             "equalizer=f=2800:t=q:w=1:g=2",
             "acompressor=threshold=-20dB:ratio=4:attack=5:release=120:makeup=2"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", ",".join(c for c in chain if c),
                    "-ar", str(SR), "-ac", "1", dst], check=True)
    a, _ = sf.read(dst)
    a = a[:n] if len(a) >= n else np.pad(a, (0, n - len(a)))
    peak = np.abs(a).max()
    if peak > 0.98:
        a = a * (0.98 / peak)
    sf.write(dst, a, SR)
    return a.astype(np.float32)


def trim(a, thr=0.01):
    idx = np.where(np.abs(a) > thr)[0]
    if len(idx) == 0:
        return a
    return a[max(0, idx[0] - 240): idx[-1] + 1200]


def mouth_track(a):
    """RMS per video frame, smoothed and normalised to 0..1."""
    hop = SR // FPS
    n = len(a) // hop
    rms = np.sqrt(np.mean(a[: n * hop].reshape(n, hop) ** 2, axis=1))
    ref = np.percentile(rms[rms > 1e-4], 95) if np.any(rms > 1e-4) else 1
    v = np.clip(rms / ref, 0, 1)
    v = np.where(v < 0.08, 0, v)          # closed between words
    out, prev = [], 0.0
    for x in v:                            # fast open, slower close
        prev = x if x > prev else prev * 0.55 + x * 0.45
        out.append(round(float(prev), 3))
    return out


if __name__ == "__main__":
    main(sys.argv[1])
