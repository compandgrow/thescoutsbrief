# The Scout Brief — reel factory

Automated match-day Instagram Reels for **@thescoutbrief**. Scout, a cartoon gorilla analyst in a suit, breaks down the data from big-club matches: the tactical change, the best and worst player on the pitch, and banter when a rival loses.

## How it works

`/match-day` runs a team of seven agents (`.claude/agents/`):

| # | Agent | Job |
|---|---|---|
| 1 | fixture-scout | Finds finished matches of the 11 watched clubs (favourites first) |
| 2 | data-collector | Pulls lineups, stats, player stats, events, shots/xG from PitchAPI |
| 3 | match-analyst | Tactical change, best/worst player, banter material, every number sourced |
| 4 | scriptwriter | 35–50 s script with a hook and emotion cues for the presenter |
| 5 | producer | Voice, lip-sync, music, animated cards, 1080×1920 MP4 |
| 6 | reviewer | Watches the frames, fact-checks every number, checks banter limits |
| 7 | publisher | Posts to @thescoutbrief via Zernio (draft for approval by default) |

**Favourites:** Man United, Real Madrid, PSG, Bayern. **Rivals** (banter when they lose): Liverpool, Man City, Chelsea, Arsenal, Spurs, Barcelona, Atlético. Settings in `config/teams.json`.

## Setup (cloud environment)

1. **Allowed domains:** `*.r2.cloudflarestorage.com` (Zernio video upload, working), later `api.pitchapi.dev` (match data). `api.firecrawl.dev` (web research). `huggingface.co`, `*.hf.co` (IndexTTS 2.5 emotional voice; also add a reference clip at `assets/voice/scout_reference.wav`).
2. **Environment variables:** `PITCHAPI_API_KEY` (from pitchapi.dev), `FIRECRAWL_API_KEY` (from firecrawl.dev, free tier 1,000 credits/month).
3. In a session: `bash setup.sh` installs dependencies and the offline voice model.

## Try it

```bash
bash setup.sh
python3 engine/voice.py reels/demo-presenter/reel.json
python3 engine/music.py reels/demo-presenter/reel.json
node engine/render.js reels/demo-presenter          # -> reels/demo-presenter/out/reel.mp4
```

The demo reels use clearly labelled fake numbers, not real matches.
