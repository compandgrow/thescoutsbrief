---
name: match-day
description: Run The Scout Brief match-day pipeline — find finished matches of the watched clubs, fetch data, analyse, script, produce the animated gorilla reel with IndexTTS emotion, review it, and hand it over for posting. Use when asked to run match day, make a reel for a match, or when a scheduled run fires.
---
# Match-day pipeline

Arguments: none (auto: every finished match that qualifies today), a match id (one match), or `schedule` (only list fixtures).

## 0. Preflight
- **Performance review first (no setup, no Firecrawl):** run the `performance-analyst` agent. It reviews every reel posted 24 h+ ago and updates `data/performance/learnings.md`. Do this even when no match is ready.
- Check for work FIRST (fast, no install needed): `python3 engine/web_data.py fixtures` then `python3 engine/web_data.py due`. If `data/queue.json` → `ready` is empty, report the `later_today` kickoffs, commit the records and stop. No setup needed.
- Only when something is ready: `bash setup.sh` (idempotent; a fresh container needs ~30 min: PyTorch + IndexTTS models).
- Data source: PitchAPI if `PITCHAPI_API_KEY` is set and `api.pitchapi.dev` answers; otherwise the **web path** (Firecrawl, needs `FIRECRAWL_API_KEY`). Check budget: `python3 engine/research.py usage`.
- Voice: IndexTTS if installed + `assets/voice/scout_reference.wav`; else the offline Echo voice (say so in the report).

## 1. Team flow — one match at a time, favourites first
| Step | Agent | Output | Gate |
|---|---|---|---|
| 1 | `fixture-scout` | `data/queue.json` | `ready` empty → report `later_today` kickoffs and stop |
| 2 | `data-collector` | `data/matches/<id>/` + `_overview.md` | score, team stats and either shots or lineups present |
| 3 | `match-analyst` | `insights.json` (+ `analysis.py`) | every number has a `source` |
| 3b | `trend-scout` | `data/matches/<id>/trends.json` (+ `data/form/<team>.json`) | every talking point has 2 trusted outlets, 1 official source, or computed form; ≤ 14 credits. Empty is fine |
| 4 | `scriptwriter` | `reels/<id>/reel.json` (with `match.league`), `caption.txt` | follows `config/format.json` (beats, words, hook payoff in 3 s) |
| 5 | `producer` | `reels/<id>/out/reel.mp4` | renders, within `format.json` duration max |
| 6 | `reviewer` | `reels/<id>/review.md` | PASS. FIX → back to 4/5, max 2 rounds, then escalate |
| 7 | approval | — | see below |
| 8 | `publisher` | Zernio post (scheduled +60 min) | reviewer PASS only |

Files are the hand-off between agents. Add each finished match to `data/state.json` → `done` (with `espn_id`), or `skipped` with the reason, so it is never made twice.

## 2. Approval (config/teams.json → `approval`, currently "auto")
- `"auto"`: after PASS, the publisher uploads to Zernio and **schedules** the post `post_delay_minutes` (60) ahead. The user is notified with the MP4 and can cancel in Zernio within that hour. Only reels with a reviewer PASS are ever scheduled.
- `"ask"`: the publisher saves a Zernio **draft** instead; the user publishes.
- If the Zernio tools aren't available in the session, nothing is posted: send the MP4 + caption to the user and say so.

## 3. Finish
- Commit and push to branch `scout-brief-v1`: `data/state.json`, `data/fixtures.json`, `data/queue.json`, `data/research/usage.json`, `data/form/*.json`, `data/performance/` (reviews, raw stats, learnings.md), `data/matches/<id>/{insights.json,trends.json,analysis.py,shots_espn.json,_web_sources.json,_overview.md}`, `reels/<id>/{reel.json,caption.txt,review.md,timing.json,mouth.json}`. Videos and audio stay out of git.
- Report: 24 h reviews (views, hook skip rate, main reason, top learning), matches made (hook line, trend angle used, best/worst, review verdict), matches skipped and why, next kickoffs, credits used, anything that failed.

## Favourites and banter
Favourites: Man United, Real Madrid, PSG, Bayern. Rival defeats get a laughing banter beat (louder if a favourite beat them). No banter when a favourite loses.

## Rules
- No fabricated data. Missing data → the reel says less.
- Anger is about performance numbers only. Banter red lines in `config/teams.json`.
- Never post to @compandgrow.
