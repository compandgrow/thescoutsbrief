"""Compose a music bed + hits in code, duck it under the voice, write mix.wav.

usage: python3 engine/music.py reels/<id>/reel.json
Needs audio/voice.wav and timing.json (run voice.py first).
"""
import json, os, sys
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 44100
BPM = 112
rng = np.random.default_rng(7)


def lp(x, f, o=2):
    return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)


def hp(x, f, o=2):
    return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)


def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(t / a, 1) * np.exp(-t / d)


def kick():
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 45 + 105 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.12)


def hat():
    n = int(0.06 * SR)
    return hp(rng.standard_normal(n), 7000) * env(n, 0.001, 0.015) * 0.25


def clap():
    n = int(0.2 * SR)
    x = sosfilt(butter(2, [900, 2500], "band", fs=SR, output="sos"), rng.standard_normal(n))
    return x * env(n, 0.002, 0.05) * 0.5


def saw(f, n):
    t = np.arange(n) / SR
    return 2 * ((t * f) % 1) - 1


def impact():
    n = int(1.6 * SR); t = np.arange(n) / SR
    sub = np.sin(2 * np.pi * (60 * np.exp(-t * 2)) * t) * np.exp(-t * 2.5)
    crash = hp(rng.standard_normal(n), 3000) * np.exp(-t * 3) * 0.3
    return sub + crash


def rumble():
    """low growl for angry beats"""
    n = int(1.2 * SR); t = np.arange(n) / SR
    x = lp(saw(41, n) + saw(41.7, n), 300) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t))
    return x * np.minimum(t / 0.05, 1) * np.exp(-t * 1.6) * 0.6


def place(buf, clip, at, g=1.0):
    i = int(at * SR)
    if i >= len(buf) or i < 0:
        return
    j = min(len(buf), i + len(clip))
    buf[i:j] += clip[: j - i] * g


def main(path):
    reel = json.load(open(path))
    d = os.path.dirname(os.path.abspath(path))
    timing = json.load(open(os.path.join(d, "timing.json")))
    dur = timing["duration"]
    n = int(dur * SR)
    beat = 60 / BPM
    music = np.zeros(n)

    # minor progression: Am F C G as root freqs
    roots = [110.0, 87.31, 130.81, 98.0]
    bar = beat * 4
    for b in range(int(dur / bar) + 1):
        f = roots[b % 4]
        seg = int(bar * SR)
        pad = sum(saw(f * m * (1 + dt), seg) for m in (1, 1.5, 2) for dt in (-0.004, 0.004))
        pad = lp(pad, 900) * 0.035
        place(music, pad, b * bar)
        bass = lp(saw(f / 2, seg), 220) * 0.12
        place(music, bass * (0.5 + 0.5 * np.cos(2 * np.pi * np.arange(seg) / SR / beat) ** 2), b * bar)

    t = 0.0
    k, h, c = kick(), hat(), clap()
    while t < dur - 0.5:
        place(music, k, t, 0.55)
        place(music, h, t + beat / 2, 1)
        if int(round(t / beat)) % 2 == 1:
            place(music, c, t, 0.6)
        t += beat

    # hits: impact on the hook, rumble on angry beats
    hits = np.zeros(n)
    place(hits, impact(), 0.25, 0.7)
    for bt, info in zip(reel["beats"], timing["beats"]):
        if bt.get("emotion") in ("angry", "furious"):
            place(hits, rumble(), info["start"] - 0.05, 0.9)
        if bt.get("hit"):
            place(hits, impact(), info["start"] - 0.05, 0.6)

    # fade out
    fade = int(1.2 * SR)
    music[-fade:] *= np.linspace(1, 0, fade)

    voice, vsr = sf.read(os.path.join(d, "audio/voice.wav"))
    voice = np.interp(np.arange(n) / SR, np.arange(len(voice)) / vsr, voice)

    # duck: moving-average envelope via cumulative sum
    w = int(0.25 * SR)
    cs = np.cumsum(np.abs(voice))
    e = (cs[w:] - cs[:-w]) / w
    e = np.concatenate([np.full(w, e[0]), e])
    duck = 1 - 0.6 * np.clip(e / (0.25 * e.max() + 1e-9), 0, 1)
    mix = voice * 1.0 + music * duck + hits * 0.8
    mix = mix / max(1.0, np.abs(mix).max() / 0.97)
    sf.write(os.path.join(d, "audio/mix.wav"), np.stack([mix, mix], 1), SR)
    print("mix", round(dur, 2), "s")


if __name__ == "__main__":
    main(sys.argv[1])
