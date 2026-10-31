# Review: manchester-united-chelsea-2026-10-31 (round 0)
Verdict: PASS

Checks
1. Facts: hook 1.10 v 0.28, 2nd half 0.08 v 2.39, shots 3 v 11 recomputed from shots_espn.json + ESPN shot 19 (Palmer pen 0.79) via analysis.py/derived.json. Rogers 50', Palmer 64' pen (ESPN header). Martinez second yellow 63' and fan rating 2.23 (lowest of both sides), from cached BBC page scrape_641adff637d5.json. Penalty xG 0.79 at 1-0 in 64th minute OK. Labelled "BBC fan rating", not official.
2. Frames (review_a/review_b/probe): no clipped text, no empty cards, first frame is the hook card, emotions fit (shocked, disappointed, angry then furious, happy).
3. Hook: 9 spoken words, first frame shows 1.10 v 0.28. First number said by about 2 s, the contrast completes at 3.9 s (timing.json beat 0 ends 3.90). Marginal against the 3 s payoff rule; accepted, noted.
4. Tone: anger aimed at performance numbers (penalty xG, rating), no personal insults, no pundit "liability" quote used.
5. Banter: favourite (MUN) lost, banter false: no banter beat, none present.
6. Trends: only t1 (three defeats in a row, no wins in last six, data/form/360.json LLLDLD, no gaps, strong). Recounted. Nothing from rejected.
7. Specs: 1080x1920, h264 + aac, 40.03 s (max 50), 7 beats (5-8), 102 -> 77 spoken words (max 110), -14.7 LUFS.
8. Caption: exists, first line 8 words with question, 10 hashtags, all numbers match insights.json.
