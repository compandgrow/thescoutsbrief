# What works on @thescoutbrief
Updated 2026-11-03 · 9 reels reviewed · confidence: medium (5-14)

Early days: nine reels, all with 156-198 views, one share, no saves and no comments in total. Patterns below are first signals, not proof. Format changes were not made (format v1 has fewer reels than its judge_after_reels).

## Rules (strongest evidence first)
- Say the payoff in the first 3 s, in 10 words or fewer, and end the hook on it; never end a hook on the resolution or final score. Evidence: mun-bou (17 words, 9.2 s hook, payoff last) 73.9% skipped; chelsea-liverpool (14 words, 6.7 s, result last) 75.5% skipped; magdeburg-bayern (9 words, 3.5 s) 62.8% skipped, the best of the three. Confidence: medium
- Shorter reels held better: 47 s reel watch ratio 0.123 against 0.071 (61 s) and 0.057 (63 s). Keep reels to about 30-40 s and drop beats after the first 25 s, since nobody reaches them (avg watch 3.6-5.8 s). Evidence: all three reels. Confidence: low
- Lead the hook with a number or contrast, not an absence ("Kane never played") or a puzzle ("18 penalties"). The Bayern hook still lost 63% in 3 s with zero shares/saves. Evidence: magdeburg-bayern, chelsea-liverpool. Confidence: low
- Don't re-read on the next beat what the hook card already shows (the score, the same stat). Viewers left during that beat on magdeburg-bayern (beat 1, 4.3-11.5 s). Evidence: 1 reel. Confidence: low


- Best so far: brighton-man city (5-word contrast hook 'Twenty-one shots. Zero goals.', 32 s, banter): skip 51.4%, watch ratio 0.199. Worst v2 hook: man-utd-chelsea bare decimals 'One point one zero. Nought point two eight.' skip 66.9%. Name the subject and use whole-number contrasts. Evidence: 2 reels. Confidence: low

- Best hold so far: borussia-dortmund-bayern (named-subject number contrast 'Four point four six xG, against zero point six three.', 37.9 s): skip 59.1%, avg watch 6.95 s (ratio 0.188), the only share (6.1/1k reach). But the twist ('Bayern still drew') came at ~12 s, after the average viewer left in beat 1 (5.7-12.7 s, a shots/box-touches stat dump). Put the twist inside the hook and follow it with the surprise_stat, not a second stat table. Evidence: 1 reel, plus bare decimals failing on man-utd-chelsea (66.9%). Confidence: low

- Bare absence endings fail even with a number first: real-madrid-racing ('Three goals, thirty-six minutes. Then nothing.', 7 words, 3.6 s) 67.6% skipped, worse than the 64.9% median, while its real twist (10 shots/3 goals before the 37th minute, 12 shots/0 goals after, insights.json) sat at 18 s. Put the twist inside the hook as two matched numbers and cut the compare beat that follows (viewers left in it at 4.4-9.7 s). Evidence: 1 reel plus the magdeburg-bayern absence hook (62.8%). Confidence: low

- Best hold and second-best hook: arsenal-liverpool ('Seventeen shots. Zero on target.', 5 words, 3.3 s, 28.7 s reel, banter): skip 54.7%, avg watch 7.68 s, watch ratio 0.274, the only reel above the 0.25 bar. Short named-subject number contrast plus a short cut works; viewers still left in beat 1 (a three-stat compare, 4.1-10.2 s) and never reached the banter beat (10.5 s). Put the banter or twist right after the hook, as beat 1, and keep the compare card to 2 rows. Evidence: arsenal-liverpool, brighton-man city (51.4%, same hook shape). Confidence: medium for the hook shape, low for the beat order

## Experiments to run next
- Hook from `surprise_stat` or the `best_angle` in trends.json, 10 words or fewer, result last-or-absent. Success: skip rate below 60% and watch ratio above 0.15 on the next 2-3 reels. Baseline 62.8-75.5%, 0.057-0.123.
- 30-35 s cut (hook, one compare card, best/worst, outro question). Success: watch ratio above 0.25. Baseline 0.071 median.
- Post within 24 h of full time. All three so far went out 32 h to 3 days after the match; compare once there are 3+ reels in each group.
- Banter or twist as beat 1 (starts by ~4 s, right after the hook) with a 2-row compare card after it, 24-30 s total. Success: avg watch above the beat 1 end and a first comment or share. Banter has sat at 10.5 s on arsenal-liverpool and nobody reaches it. Measure with comments and shares per 1k reach (baseline 0).

## Channel baseline
Medians from `performance.py table` (9 reels): views 167 · reach 157 · avg watch 5.2 s · watch ratio 0.153 · skip rate 62.8% · completion n/a (0) · engagements 0.0/1k reach · shares+saves 0.0/1k reach · follows n/a (Zernio returned null; timeline shows 0)
