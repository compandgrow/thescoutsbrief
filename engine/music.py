"""Compose a music bed + hits in code, duck it under the voice, write mix.wav.

usage: python3 engine/music.py reels/<id>/reel.json [--style match|noir|thriller]
Needs audio/voice.wav and timing.json (run voice.py first).

Styles: "match" (punchy minor beat, match reels), "noir" (swung detective jazz: walking bass, brushes,
Rhodes chords, vinyl), "thriller" (dark pulse, ticking clock, rising strings). Picked from --style, then
reel.json "music", then the series default (scout-files -> config/stories.json music_style, else match).
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


def sine(f, n, ph=0.0):
    return np.sin(2 * np.pi * f * np.arange(n) / SR + ph)


def pluck_bass(f, length):
    n = int(length * SR); t = np.arange(n) / SR
    x = sine(f, n) + 0.35 * sine(2 * f, n) + 0.12 * sine(3 * f, n)
    return lp(x, 500) * np.minimum(t / 0.006, 1) * np.exp(-t / 0.32)


def rhodes(freqs, length):
    n = int(length * SR); t = np.arange(n) / SR
    out = np.zeros(n)
    for f in freqs:
        out += (sine(f, n) + 0.25 * sine(2 * f, n) * np.exp(-t * 6) + 0.08 * sine(7 * f, n) * np.exp(-t * 20))
    trem = 0.85 + 0.15 * np.sin(2 * np.pi * 4.5 * t)
    return out * trem * np.minimum(t / 0.01, 1) * np.exp(-t / 1.6) / max(1, len(freqs))


def ride():
    n = int(0.6 * SR); t = np.arange(n) / SR
    metal = sum(sine(f, n) for f in (3150, 4420, 5870, 7330)) * 0.15 + hp(rng.standard_normal(n), 6000) * 0.5
    return metal * env(n, 0.001, 0.22) * 0.18


def brush():
    n = int(0.25 * SR); t = np.arange(n) / SR
    x = sosfilt(butter(2, [1800, 6000], "band", fs=SR, output="sos"), rng.standard_normal(n))
    return x * np.minimum(t / 0.03, 1) * np.exp(-t / 0.07) * 0.35


def vinyl(n):
    hiss = lp(rng.standard_normal(n), 5000) * 0.006
    clicks = np.zeros(n)
    for i in rng.integers(0, n, size=max(1, n // SR * 3)):
        clicks[i:i + 30] += rng.standard_normal(min(30, n - i)) * 0.08
    return hiss + lp(clicks, 3000)


NOTE = lambda m: 440.0 * 2 ** ((m - 69) / 12)


def bed_noir(dur):
    """Swung detective jazz in D minor: Dm9 | Gm9 | Em7b5 | A7b9."""
    bpm, n = 88, int(dur * SR)
    beat, music = 60 / bpm, np.zeros(n)
    chords = [[50, 53, 57, 60, 64], [55, 58, 62, 65, 69], [52, 55, 58, 62], [57, 61, 64, 67, 70]]
    walks = [[38, 41, 45, 44], [43, 46, 50, 49], [40, 43, 46, 44], [45, 49, 52, 37]]
    bar = beat * 4
    for b in range(int(dur / bar) + 1):
        c = b % 4
        place(music, rhodes([NOTE(m) for m in chords[c]], bar * 1.1), b * bar, 0.16)
        place(music, rhodes([NOTE(m) for m in chords[c][1:4]], beat * 1.2), b * bar + beat * 2.66, 0.08)   # comp on the "and" of 3
        for q, m in enumerate(walks[c]):
            place(music, pluck_bass(NOTE(m), beat * 1.1), b * bar + q * beat, 0.32)
        if b % 2 == 1:   # vibraphone motif every other bar
            for k, m in enumerate([74, 77, 76, 72]):
                nn = int(beat * 0.9 * SR); tt = np.arange(nn) / SR
                place(music, sine(NOTE(m), nn) * (1 + 0.004 * np.sin(2 * np.pi * 5 * tt)) * np.exp(-tt / 0.5) * 0.05, b * bar + k * beat * 0.66 + beat)
    t, r, br, kk = 0.0, ride(), brush(), kick()
    sw = beat * 2 / 3                              # swing: second eighth lands at 2/3 of the beat
    while t < dur - 0.5:
        i = int(round(t / beat))
        place(music, r, t, 0.9)
        if i % 2 == 1:
            place(music, r, t + sw, 0.6)
            place(music, br, t, 1.0)
        if i % 4 == 0:
            place(music, kk, t, 0.18)
        t += beat
    return music + vinyl(n)


def bed_thriller(dur):
    """Dark pulse: low eighth-note ostinato, ticking clock, slow rising strings."""
    bpm, n = 100, int(dur * SR)
    beat, music = 60 / bpm, np.zeros(n)
    roots = [NOTE(38), NOTE(38), NOTE(34), NOTE(36)]   # D D Bb C
    bar = beat * 4
    for b in range(int(dur / bar) + 1):
        f = roots[b % 4]
        for e8 in range(8):
            nn = int(beat / 2 * SR); tt = np.arange(nn) / SR
            g = 0.16 if e8 % 2 == 0 else 0.1
            place(music, lp(saw(f, nn) + saw(f * 1.003, nn), 380) * np.exp(-tt / 0.18) * g, b * bar + e8 * beat / 2)
        seg = int(bar * SR); tt = np.arange(seg) / SR
        strings = sum(saw(NOTE(m) * (1 + dt), seg) for m in (62, 65, 69) for dt in (-0.003, 0.003))
        place(music, lp(strings, 700 + 500 * ((b % 4) / 3)) * 0.02 * (0.6 + 0.4 * np.sin(np.pi * tt / (bar))), b * bar)
    t, h = 0.0, hat()
    while t < dur - 0.5:
        place(music, h, t, 0.7)                       # tick
        place(music, h, t + beat / 2, 0.35)           # tock
        if int(round(t / beat)) % 4 == 0:
            place(music, kick(), t, 0.4)
        t += beat
    sub = sine(NOTE(26), n) * 0.05
    return music + sub


def bed_match(dur):
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
    return music


def pick_style(reel, forced=None):
    if forced:
        return forced
    if reel.get("music"):
        return reel["music"]
    if reel.get("series") == "scout-files" or reel.get("presenter") == "detective3d":
        try:
            return json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config/stories.json"))).get("music_style", "noir")
        except FileNotFoundError:
            return "noir"
    return "match"


def main(path, forced=None):
    reel = json.load(open(path))
    d = os.path.dirname(os.path.abspath(path))
    timing = json.load(open(os.path.join(d, "timing.json")))
    dur = timing["duration"]
    n = int(dur * SR)
    style = pick_style(reel, forced)
    music = {"match": bed_match, "noir": bed_noir, "thriller": bed_thriller}[style](dur)[:n]
    if len(music) < n:
        music = np.pad(music, (0, n - len(music)))

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
    print("mix", round(dur, 2), "s", "style", style)


if __name__ == "__main__":
    args = sys.argv[1:]
    forced = args[args.index("--style") + 1] if "--style" in args else None
    main(args[0], forced)
