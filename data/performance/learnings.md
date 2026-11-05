# What works on @thescoutbrief
Updated 2026-11-05 · 12 reels reviewed · confidence: medium (5-14)

Early days: twelve reels, all with 156-198 views, one share, two saves and no comments in total. Patterns below are first signals, not proof. Format changes were not made (format v2 has nine reels reviewed, no clear failure; no skip rate above 75% or watch ratio below 0.1 in v2).

## Rules (strongest evidence first)
- Open on a short number contrast that names the subject, with the payoff inside 4 s: 5 to 10 words, the number or the contrast first, never ending on the resolution or a bare absence. Evidence: bayern-atletico "Nineteen shots to nine. Atlético's unbeaten run: over." (9 words) 49.6% skipped, brighton-man city "Twenty-one shots. Zero goals." 51.4%, arsenal-liverpool "Seventeen shots. Zero on target." 54.7%, psg-villarreal (10 words) 56.6%; against mun-bou (17 words) 73.9%, chelsea-liverpool (14 words, result last) 75.5%, man-utd-chelsea bare decimals 66.9%, real-madrid-racing "Then nothing." 67.6%. Confidence: medium
- Keep reels to about 30 s; nobody reaches past the first ~8 s. Evidence: avg watch 6.5-7.7 s on the five reels of 28-40 s with watch ratio 0.18-0.27, against 3.6-5.8 s and 0.057-0.123 on the 47-63 s reels; arsenal-liverpool (28.7 s) 0.274, roma-man utd (31.4 s) 0.234, psg-villarreal (30.2 s) 0.218, bayern-atletico (40.4 s) 0.176. Confidence: medium
- Beat 1 is where viewers leave (4-12 s), in every v2 reel. Never spend it on a stat table that repeats the hook card; use it for the twist, the banter or the story. Evidence: psg-villarreal (5.7-10.6 s compare), roma-man utd (4.1-11.0 s compare), arsenal-liverpool (4.1-10.2 s compare), dortmund-bayern (5.7-12.7 s stat dump), real-madrid-racing (compare), magdeburg-bayern (4.3-11.5 s). Confidence: medium
- Put the twist or the banter right after the hook, as beat 1. Banter at beat 1 (5.5 s) was reached by the average viewer (7.0 s) on bayern-atletico; banter at 10.5 s on arsenal-liverpool was not. Whether banter wins comments or shares is still unproven (0 comments across 12 reels). Evidence: bayern-atletico, arsenal-liverpool. Confidence: low
- Put the trend with `use_for: hook` in the hook (the streak, drought or milestone number), with the match twist second. roma-man utd opened on the opponent's pair ("Seven Roma shots before half-time. Zero after.", 57.7%) and left the nine-game winless run (the trend) to beat 2 at 11 s, after the average viewer (7.3 s) left. Evidence: 1 reel. Confidence: low
- Ask a two-name question with a side in the outro and the caption, and say it before the average viewer leaves if the reel is long. Evidence: only dortmund-bayern (6.1 shares+saves/1k reach, share rate) and psg-villarreal (5.7/1k, one save) got any shares/saves; both were reels with a fan_question; bayern-atletico asked "Kane or Laimer?" at 33 s and got 0. Zero comments on any reel so far, so the outro question has not worked yet. Confidence: low
- Don't re-read on the next beat what the hook card already shows (the score, the same stat). Evidence: magdeburg-bayern beat 1, psg-villarreal beat 1, roma-man utd beat 1. Confidence: medium
- Put the twist inside the hook as two matched numbers; "the real story at 12-18 s" never lands. Evidence: dortmund-bayern twist ("Bayern still drew") at ~12 s, real-madrid-racing twist (10 shots/3 goals before the 37th minute, 12/0 after) at 18 s, both after the average viewer left. Confidence: low

## Experiments to run next
- 28-30 s cut with banter or the twist as beat 1 (under 10 words, starts by ~4 s), the compare card cut to 2 rows or dropped, and the outro question moved to the second half of the reel. Success: watch ratio above 0.25, first comment or share. Baseline watch ratio 0.173, shares+saves 0.0.
- Open on the hook-flagged trend number (use_for: hook) plus the match twist in one sentence, 10-12 words. Success: skip below 52%. Baseline 58.4% median, best 49.6%.
- Post within 24 h of full time. Every v2 reel has gone out 20-26 h after the match; the 01 UTC slot gives skip 49.6-59.1%, the 19-20 UTC slot 51.4-67.6%. Not enough data to pick a slot.
- Fan-driven angle: angle_source is still null or talking_point/data on every reel (Reddit keys unset), so there is no fan_buzz reel to compare yet.

## Channel baseline
Medians from `performance.py table` (12 reels): views 173 · reach 158.5 · avg watch 6.07 s · watch ratio 0.173 · skip rate 58.4% · completion n/a (0) · engagements 6.1/1k reach · shares+saves 0.0/1k reach · follows n/a (Zernio returned null; timeline shows 0)
