"""Voice the script offline with Kokoro and build the lip-sync track.

usage: python3 engine/voice.py reels/<id>/reel.json

Writes next to reel.json:
  audio/voice.wav   full narration on one timeline
  timing.json       start/end seconds per beat
  mouth.json        mouth openness 0..1 per frame (FPS below)
"""
import json, sys, os, re, subprocess, tempfile
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

FPS = 30
SR = 24000
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Emotion = a performance profile. Kokoro has no emotion input, so each profile sets:
#   mix    voice blend (base voice + a more energetic/playful one)
#   speed  pace;  pitch  semitones (formants preserved, so it sounds like inflection, not an effect)
#   gain   loudness;  pause  silence between sentences;  grit  0..1 vocal strain for anger
STYLE = {
    "neutral":      {"mix": {"am_onyx": 1.0},                    "speed": 1.06, "pitch":  0.0, "gain": 1.00, "pause": 0.16, "grit": 0},
    "smug":         {"mix": {"am_onyx": 0.8, "am_puck": 0.2},     "speed": 0.96, "pitch": -0.7, "gain": 1.00, "pause": 0.30, "grit": 0},
    "happy":        {"mix": {"am_onyx": 0.7, "am_puck": 0.3},     "speed": 1.08, "pitch":  1.0, "gain": 1.10, "pause": 0.20, "grit": 0},
    "excited":      {"mix": {"am_onyx": 0.6, "am_fenrir": 0.4},   "speed": 1.13, "pitch":  1.8, "gain": 1.20, "pause": 0.16, "grit": 0},
    "shocked":      {"mix": {"am_onyx": 0.7, "am_fenrir": 0.3},   "speed": 1.04, "pitch":  1.6, "gain": 1.15, "pause": 0.26, "grit": 0},
    "disappointed": {"mix": {"am_onyx": 1.0},                    "speed": 0.94, "pitch": -1.6, "gain": 0.85, "pause": 0.30, "grit": 0},
    "laughing":     {"mix": {"am_onyx": 0.6, "am_puck": 0.4},     "speed": 1.10, "pitch":  1.5, "gain": 1.15, "pause": 0.18, "grit": 0},
    "angry":        {"mix": {"am_onyx": 0.6, "am_fenrir": 0.4},   "speed": 1.10, "pitch":  1.0, "gain": 1.40, "pause": 0.18, "grit": 0.5},
    "furious":      {"mix": {"am_onyx": 0.5, "am_fenrir": 0.5},   "speed": 1.16, "pitch":  2.2, "gain": 1.60, "pause": 0.14, "grit": 1.0},
}
LEAD_IN = 0.45   # silence before first line
GAP = 0.32       # silence between lines
TAIL = 0.9       # silence after the last line


def main(path):
    reel = json.load(open(path))
    out_dir = os.path.dirname(os.path.abspath(path))
    os.makedirs(os.path.join(out_dir, "audio"), exist_ok=True)
    k = Kokoro(os.path.join(ROOT, "models/kokoro-v1.0.onnx"),
               os.path.join(ROOT, "models/voices-v1.0.bin"))
    cfg = json.load(open(os.path.join(ROOT, "config/teams.json"))).get("voice", {})
    fx = {**cfg, **reel.get("voice_fx", {})}

    pieces, timing, t = [], [], LEAD_IN
    pieces.append(np.zeros(int(LEAD_IN * SR), np.float32))
    styles = {}
    def style_of(mix):
        key = tuple(sorted(mix.items()))
        if key not in styles:
            styles[key] = sum(k.get_voice_style(v) * w for v, w in mix.items()).astype(np.float32)
        return styles[key]

    for i, beat in enumerate(reel["beats"]):
        emo = beat.get("emotion", "neutral")
        st = {**STYLE.get(emo, STYLE["neutral"]), **beat.get("voice_style", {})}
        sentences = [x.strip() for x in re.findall(r"[^.!?]+[.!?]*", beat["say"]) if x.strip()]
        parts = []
        for j, sen in enumerate(sentences):
            a, sr = k.create(sen, voice=style_of(st["mix"]), speed=beat.get("speed", st["speed"]), lang="en-us")
            assert sr == SR
            # intonation: exclamations lift, sentences alternate slightly so lines don't drone
            semi = st["pitch"] + (0.8 if sen.endswith("!") else 0) + (0.35 if j % 2 == 0 else -0.35) * (len(sentences) > 1)
            a = perform(trim(a), semi, st["grit"]) * st["gain"]
            parts.append(a)
            if j < len(sentences) - 1:
                parts.append(np.zeros(int(st["pause"] * SR), np.float32))
        audio = np.concatenate(parts)
        dur = len(audio) / SR
        timing.append({"beat": i, "start": round(t, 3), "end": round(t + dur, 3)})
        pieces.append(audio.astype(np.float32))
        gap = beat.get("pause_after", GAP)
        pieces.append(np.zeros(int(gap * SR), np.float32))
        t += dur + gap
        print(f"beat {i:2d} {emo:12s} {dur:5.2f}s  {beat['say'][:60]}")
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
             "acompressor=threshold=-18dB:ratio=2.2:attack=8:release=150:makeup=1.5"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", ",".join(c for c in chain if c),
                    "-ar", str(SR), "-ac", "1", dst], check=True)
    a, _ = sf.read(dst)
    a = a[:n] if len(a) >= n else np.pad(a, (0, n - len(a)))
    peak = np.abs(a).max()
    if peak > 0.98:
        a = a * (0.98 / peak)
    sf.write(dst, a, SR)
    return a.astype(np.float32)


def perform(a, semi, grit):
    """Per-sentence delivery: natural pitch inflection (formants preserved) and vocal strain for anger."""
    if abs(semi) < 0.05 and grit == 0:
        return a
    chain = []
    if abs(semi) >= 0.05:
        chain.append(f"rubberband=pitch={2 ** (semi / 12):.5f}:formant=preserved:pitchq=quality")
    if grit:
        chain += [f"equalizer=f=2200:t=q:w=1.2:g={3 * grit:.1f}",          # shouty presence
                  f"asoftclip=type=tanh:threshold={1 - 0.35 * grit:.2f}"]   # slight strain, not distortion
    with tempfile.TemporaryDirectory() as d:
        src, dst = os.path.join(d, "in.wav"), os.path.join(d, "out.wav")
        sf.write(src, a, SR)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", ",".join(chain), "-ar", str(SR), "-ac", "1", dst], check=True)
        b, _ = sf.read(dst)
    return b.astype(np.float32)


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
