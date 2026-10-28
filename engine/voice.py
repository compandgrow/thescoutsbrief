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

# Emotion = a performance profile for the offline voice. Pure Echo only: no voice blending and
# no pitch processing (both sounded like autotune). Emotion comes from pace, pauses and loudness.
STYLE = {
    "neutral":      {"mix": {"am_echo": 1.0}, "speed": 1.06, "pitch": 0, "gain": 1.00, "pause": 0.16, "grit": 0},
    "smug":         {"mix": {"am_echo": 1.0}, "speed": 0.98, "pitch": 0, "gain": 1.00, "pause": 0.28, "grit": 0},
    "happy":        {"mix": {"am_echo": 1.0}, "speed": 1.10, "pitch": 0, "gain": 1.10, "pause": 0.16, "grit": 0},
    "excited":      {"mix": {"am_echo": 1.0}, "speed": 1.15, "pitch": 0, "gain": 1.20, "pause": 0.12, "grit": 0},
    "shocked":      {"mix": {"am_echo": 1.0}, "speed": 1.04, "pitch": 0, "gain": 1.15, "pause": 0.30, "grit": 0},
    "disappointed": {"mix": {"am_echo": 1.0}, "speed": 0.94, "pitch": 0, "gain": 0.85, "pause": 0.32, "grit": 0},
    "laughing":     {"mix": {"am_echo": 1.0}, "speed": 1.12, "pitch": 0, "gain": 1.15, "pause": 0.14, "grit": 0},
    "angry":        {"mix": {"am_echo": 1.0}, "speed": 1.12, "pitch": 0, "gain": 1.35, "pause": 0.14, "grit": 0},
    "furious":      {"mix": {"am_echo": 1.0}, "speed": 1.18, "pitch": 0, "gain": 1.55, "pause": 0.10, "grit": 0},
}
LEAD_IN = 0.45   # silence before first line
GAP = 0.32       # silence between lines
TAIL = 0.9       # silence after the last line


def main(path):
    reel = json.load(open(path))
    out_dir = os.path.dirname(os.path.abspath(path))
    os.makedirs(os.path.join(out_dir, "audio"), exist_ok=True)
    cfg = json.load(open(os.path.join(ROOT, "config/teams.json"))).get("voice", {})
    fx = {**cfg, **reel.get("voice_fx", {})}
    beat_audio = None
    if cfg.get("engine") == "indextts":
        beat_audio = indextts_beats(reel["beats"], cfg.get("indextts", {}), out_dir)
        if beat_audio is not None:
            fx = {**fx, "pitch": 0}          # real performance: no pitch processing on top
    if beat_audio is None:
        beat_audio = kokoro_beats(reel["beats"])

    pieces, timing, t = [], [], LEAD_IN
    pieces.append(np.zeros(int(LEAD_IN * SR), np.float32))
    for i, (beat, audio) in enumerate(zip(reel["beats"], beat_audio)):
        dur = len(audio) / SR
        timing.append({"beat": i, "start": round(t, 3), "end": round(t + dur, 3)})
        pieces.append(audio.astype(np.float32))
        gap = beat.get("pause_after", GAP)
        pieces.append(np.zeros(int(gap * SR), np.float32))
        t += dur + gap
        print(f"beat {i:2d} {beat.get('emotion', 'neutral'):12s} {dur:5.2f}s  {beat['say'][:60]}")
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


# IndexTTS emotion vectors: [happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]
EMO_VECTOR = {
    "neutral":      [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.60],
    "smug":         [0.35, 0.00, 0.00, 0.00, 0.10, 0.00, 0.00, 0.30],
    "happy":        [0.70, 0.00, 0.00, 0.00, 0.00, 0.00, 0.10, 0.10],
    "excited":      [0.75, 0.00, 0.00, 0.00, 0.00, 0.00, 0.35, 0.00],
    "shocked":      [0.00, 0.00, 0.00, 0.15, 0.00, 0.00, 0.85, 0.00],
    "disappointed": [0.00, 0.00, 0.45, 0.00, 0.00, 0.40, 0.00, 0.10],
    "laughing":     [0.90, 0.00, 0.00, 0.00, 0.00, 0.00, 0.20, 0.00],
    "angry":        [0.00, 0.70, 0.00, 0.00, 0.20, 0.00, 0.00, 0.00],
    "furious":      [0.00, 0.95, 0.00, 0.00, 0.25, 0.00, 0.00, 0.00],
}


def kokoro_beats(beats):
    """Offline fallback voice: pure Echo, emotion via pace, pauses and loudness only."""
    k = Kokoro(os.path.join(ROOT, "models/kokoro-v1.0.onnx"), os.path.join(ROOT, "models/voices-v1.0.bin"))
    styles, out = {}, []

    def style_of(mix):
        key = tuple(sorted(mix.items()))
        if key not in styles:
            styles[key] = sum(k.get_voice_style(v) * w for v, w in mix.items()).astype(np.float32)
        return styles[key]

    for beat in beats:
        st = {**STYLE.get(beat.get("emotion", "neutral"), STYLE["neutral"]), **beat.get("voice_style", {})}
        sentences = [x.strip() for x in re.findall(r"[^.!?]+[.!?]*", beat["say"]) if x.strip()]
        parts = []
        for j, sen in enumerate(sentences):
            a, sr = k.create(sen, voice=style_of(st["mix"]), speed=beat.get("speed", st["speed"]), lang="en-us")
            assert sr == SR
            # intonation: exclamations lift, sentences alternate slightly so lines don't drone
            parts.append(trim(a) * st["gain"])   # untouched voice: no pitch shifting
            if j < len(sentences) - 1:
                parts.append(np.zeros(int(st["pause"] * SR), np.float32))
        out.append(np.concatenate(parts))
    return out


def indextts_beats(beats, icfg, out_dir):
    """Real emotional performance with IndexTTS 2.5 (separate venv). Returns None if it isn't installed."""
    home = icfg.get("home", "/home/user/indextts")
    py, model_dir = os.path.join(home, ".venv/bin/python"), os.path.join(home, "checkpoints")
    speaker = os.path.join(ROOT, icfg.get("speaker", "assets/voice/scout_reference.wav"))
    missing = [p for p in (py, os.path.join(model_dir, "config.yaml"), speaker) if not os.path.exists(p)]
    if missing:
        print("IndexTTS not ready, using the offline voice instead. Missing:", ", ".join(missing))
        return None
    tmp = os.path.join(out_dir, "audio/indextts")
    os.makedirs(tmp, exist_ok=True)
    import hashlib
    ref_id = hashlib.sha1(open(speaker, "rb").read()).hexdigest()[:8]
    jobs = []
    for i, b in enumerate(beats):
        emo = b.get("emotion", "neutral")
        job = {"text": b["say"], "emo_vector": b.get("emo_vector", EMO_VECTOR.get(emo, EMO_VECTOR["neutral"])),
               "emo_alpha": b.get("emo_alpha", icfg.get("emo_alpha", 0.9))}
        # cache: a line is only re-generated when its text, emotion or the reference voice changes
        key = hashlib.sha1(json.dumps([job, ref_id], sort_keys=True).encode()).hexdigest()[:12]
        job["out"] = os.path.join(tmp, f"line_{key}.wav")
        jobs.append(job)
    todo = [j for j in jobs if not os.path.exists(j["out"])]
    print(f"IndexTTS: {len(jobs) - len(todo)} lines reused, {len(todo)} to generate")
    if todo:
        spec = os.path.join(tmp, "jobs.json")
        json.dump({"model_dir": model_dir, "speaker": speaker, "jobs": todo}, open(spec, "w"), indent=1)
        subprocess.run([py, os.path.join(ROOT, "engine/indextts_worker.py"), spec], check=True)
    out = []
    for j in jobs:
        a, sr = sf.read(j["out"])
        a = a if a.ndim == 1 else a.mean(1)
        if sr != SR:   # resample to the pipeline rate
            a = np.interp(np.arange(int(len(a) * SR / sr)) * sr / SR, np.arange(len(a)), a)
        out.append(trim(a.astype(np.float32)))
    return out


def apply_fx(src, dst, fx, n):
    """Light polish only (no pitch processing): a touch of bass, presence and gentle compression."""
    chain = [f"bass=g={fx.get('bass', 2)}:f=110",
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
