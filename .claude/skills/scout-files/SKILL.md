---
name: scout-files
description: Run the Scout Files series for @thescoutbrief — every 2-3 days, pick a dramatic but true player story (trending on Reddit or in the news), research it on trusted sites, script it, produce a reel hosted by Inspector Croak (3D frog detective), review it and schedule it. Use when asked for a Scout File / player story, or when the Scout Files scheduled run fires.
---
# Scout Files run

Arguments: none (auto: make one story if it's due), `force` (make one now), or a player name (story about that player).

## 0. Is a story due?
- Read `config/stories.json` → `cadence_days` and `data/stories/state.json` → `done`. If the newest `scheduled_for` is less than `cadence_days` days ago (and no `force`/player argument), report "next Scout File due on <date>" and stop. No setup needed.
- Free scraping (about 20 s): `python3 -c "import scrapling.fetchers, markdownify" 2>/dev/null || python3 -m pip install -q "scrapling[fetchers]" markdownify`.
- `python3 engine/reddit.py digest` (free) so the story scout sees what fans are talking about today.
- `python3 engine/research.py usage`: if fewer than `credits_max_per_story` credits are left this month, stop and report it.

## 1. Flow
| Step | Agent | Output | Gate |
|---|---|---|---|
| 1 | `story-scout` | `data/stories/<id>/story.json` | every beat sourced (2 trusted outlets or 1 official); nothing from `never`. `status: no_story` → record in `skipped`, report, stop |
| 2 | `story-writer` | `reels/story-<id>/reel.json` (`presenter: frog3d`, `series: scout-files`), `caption.txt` | structure + duration from `config/stories.json`, hook payoff within 3 s |
| 2b | `story-writer` (prop) | `reels/story-<id>/props/prop.glb` + `prop` in reel.json | optional: CC0 catalogue first, else free forge; skip if both fail |
| 3 | setup | | `bash setup.sh` (voice models etc.) only now |
| 4 | `producer` | `reels/story-<id>/out/reel.mp4` | renders, ≤ `duration_s.max`; the 3D frog host (WebGL) appears in the frames |
| 5 | `reviewer` | `reels/story-<id>/review.md` | PASS (incl. the Scout Files checks). FIX → back to 2/4, max 2 rounds, then escalate |
| 6 | `publisher` | Zernio post scheduled `post_delay_minutes` ahead (approval mode from config/teams.json) | reviewer PASS only; records in `data/state.json` and `data/stories/state.json` |

## 2. Finish
- Commit and push to `scout-brief-v1`: `data/stories/`, `data/trends/`, `data/state.json`, `data/research/usage.json`, `reels/story-<id>/{reel.json,caption.txt,review.md,timing.json,mouth.json}`. Video and audio stay out of git.
- Report: the story (player, angle, hook line), sources used, review verdict, post status/time, credits used, next due date.

## Rules
- Dramatic and true, about football. Never private life, health, legal/criminal claims, rumours or cruelty (`config/stories.json` → `never`). A skipped day beats a risky post.
- Never post to @compandgrow.
