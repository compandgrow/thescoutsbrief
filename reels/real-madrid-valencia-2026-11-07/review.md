# Review: real-madrid-valencia-2026-11-07

**Verdict: PASS** (round 2)

## Previous FIX items
1. Umlaut: the player card now renders "GÜLER" with the diaeresis, in both the name and the subtitle ("ARDA GÜLER"). Checked in review_b.jpg and in a full-size frame at 20 s.
2. Hook: "Madrid, two point two six xG. Valencia, point one six." is 10 words, which is within `hook.max_words` of 10. The payoff is spoken from 0.45 s, within the 3 s limit, and frame 0 shows 2.26 and 0.16.
3. Caption: 10 hashtags, within the 6-10 limit. The debate question is in the first line. The claims match the data: Güler scored the second goal and set up Mbappé's third, and the BBC page says "Valverde opens scoring for visitors before Guler's second".

## Rechecked
- The facts were checked earlier against scrape_1a79253aa427.json (ESPN) and scrape_82fb73e8e332.json (BBC). reel.json is unchanged apart from the hook line, and every number still matches.
- Tone is clean. There is no banter, no fan_buzz claim and no trend claim.
- Specs: 1080x1920, H.264 + AAC, 33.5 s (max 50), 6 beats, -14.7 LUFS.
- The contact sheets show no clipped or overlapping text, and the captions match the cards. The first frame is the hook card.
