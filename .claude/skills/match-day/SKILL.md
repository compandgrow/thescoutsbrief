---
name: match-day
description: Run The Scout Brief match-day pipeline — find finished matches of the watched clubs, fetch data, analyse, script, produce the animated-presenter reel, review it, and post it to @thescoutbrief. Use when asked to run match day, make a reel for a match, or when a scheduled run fires.
---
# Match-day pipeline

Arguments: none (auto: every finished watched match today), or a PitchAPI match id (one match), or `schedule` (only list fixtures).

## 0. Preflight (stop with a clear message if any fails)
- `bash setup.sh` (idempotent: installs deps, downloads the voice model if missing).
- `PITCHAPI_API_KEY` set; `api.pitchapi.dev` reachable (`curl -s -o /dev/null -w '%{http_code}' https://api.pitchapi.dev`).
- Optional: `FIRECRAWL_API_KEY` set for web research (`python3 engine/research.py usage`). Without it the analyst skips research and notes it.

## 1. Team flow — run the subagents in order, one match at a time
| Step | Agent | Output | Gate |
|---|---|---|---|
| 1 | `fixture-scout` | `data/queue.json` | nothing ready → report the next kickoffs and stop |
| 2 | `data-collector` (match id) | `data/matches/<id>/` + `_overview.md` | required datasets present |
| 3 | `match-analyst` | `insights.json` | every number has a `source` |
| 4 | `scriptwriter` | `reels/<id>/reel.json`, `caption.txt` | 7–10 beats, hook in beat 1 |
| 5 | `producer` | `reels/<id>/out/reel.mp4` | renders, 25–60 s |
| 6 | `reviewer` | `reels/<id>/review.md` | PASS. On FIX: send the list to scriptwriter/producer, re-render, review again. Max 2 rounds, then escalate. |
| 7 | approval | — | see below |
| 8 | `publisher` | Zernio post | — |

Pass each agent the match id and the paths it needs; agents don't share memory, files are the hand-off.

## 2. Approval (config/teams.json → `approval`)
- `"ask"` (default): after PASS, send the user the MP4 (SendUserFile) + caption + the reviewer's notes, and have the publisher save a **draft** in Zernio. The user approves → publish/schedule the draft.
- `"auto"`: publisher schedules it `post_delay_minutes` ahead and the user is notified with the file so they can cancel.

## 3. Finish
- Commit and push `data/research/usage.json`, `reels/<id>/reel.json`, `caption.txt`, `review.md`, `data/state.json` and `data/matches/<id>/insights.json` (not the MP4/frames/audio; they're gitignored).
- Report: match, hook line, best/worst player, tactical change, review result, post status/link, anything that failed.

## Favourites and banter
Favourites: Man United, Real Madrid, PSG, Bayern (`config/teams.json`). Their matches go first. When a rival (Liverpool, Man City, Chelsea, Arsenal, Spurs, Barcelona, Atlético) loses, the reel gets a banter beat with the laughing presenter, louder when a favourite beat them. No banter when a favourite loses.

## Rules
- No fabricated data, ever. If data is missing, the reel says less; it doesn't guess.
- Anger is about performance numbers only.
- Never post to @compandgrow.
