# What works on @thescoutbrief
Updated 2026-10-30 · 3 reels reviewed · confidence: low (<5 reels)

Early days: three reels, all with 156-198 views, no shares, no saves and no comments. Patterns below are first signals, not proof. Format changes were not made (format v1 has fewer reels than its judge_after_reels).

## Rules (strongest evidence first)
- Say the payoff in the first 3 s, in 10 words or fewer, and end the hook on it; never end a hook on the resolution or final score. Evidence: mun-bou (17 words, 9.2 s hook, payoff last) 73.9% skipped; chelsea-liverpool (14 words, 6.7 s, result last) 75.5% skipped; magdeburg-bayern (9 words, 3.5 s) 62.8% skipped, the best of the three. Confidence: medium
- Shorter reels held better: 47 s reel watch ratio 0.123 against 0.071 (61 s) and 0.057 (63 s). Keep reels to about 30-40 s and drop beats after the first 25 s, since nobody reaches them (avg watch 3.6-5.8 s). Evidence: all three reels. Confidence: low
- Lead the hook with a number or contrast, not an absence ("Kane never played") or a puzzle ("18 penalties"). The Bayern hook still lost 63% in 3 s with zero shares/saves. Evidence: magdeburg-bayern, chelsea-liverpool. Confidence: low
- Don't re-read on the next beat what the hook card already shows (the score, the same stat). Viewers left during that beat on magdeburg-bayern (beat 1, 4.3-11.5 s). Evidence: 1 reel. Confidence: low

## Experiments to run next
- Hook from `surprise_stat` or the `best_angle` in trends.json, 10 words or fewer, result last-or-absent. Success: skip rate below 60% and watch ratio above 0.15 on the next 2-3 reels. Baseline 62.8-75.5%, 0.057-0.123.
- 30-35 s cut (hook, one compare card, best/worst, outro question). Success: watch ratio above 0.25. Baseline 0.071 median.
- Post within 24 h of full time. All three so far went out 32 h to 3 days after the match; compare once there are 3+ reels in each group.
- Banter beat early (inside the first 10 s) to test whether it holds viewers; at present nobody reaches it. Measure with comments and shares per 1k reach (baseline 0).

## Channel baseline
Medians from `performance.py table` (3 reels): views 178 · reach 161 · avg watch 4.3 s · watch ratio 0.071 · skip rate 73.9% · completion n/a (0) · engagements 6.2/1k reach · shares+saves 0.0/1k reach · follows n/a (Zernio returned null; timeline shows 0)
