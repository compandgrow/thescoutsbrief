# Review: real-madrid-valencia-2026-11-07

**Verdict: FIX** (round 1; all minor, facts are clean)

1. Beat 3 (player card): the name renders as "GULER", with no umlaut. The data and reel.json say "Güler", and the Anton font or uppercase transform drops the diaeresis. Fix the glyph (use a font or fallback that has Ü) and re-render. The caption and `say` are fine.
2. Beat 0 (hook): the spoken line has 11 words ("Madrid, two point two six expected goals. Valencia, point one six."), over `hook.max_words` 10. Trim to 10 or fewer, e.g. "Madrid, two point two six expected goals. Valencia, point one six." becomes "Madrid: two point two six xG. Valencia: point one six." Timing is fine, since "2.26" is said by about 2 s (limit 3 s) and frame 0 shows the payoff.
3. caption.txt: 11 hashtags, over the 6-10 limit. Drop one (e.g. #scoutbrief or #Guler). The config also wants the debate question in the caption's first line, but the first line is currently the hook. Put the question there if the hook line stays at 8 words or fewer, otherwise keep the hook and note the conflict.

## Checked and OK
- Facts, checked in data/research/scrape_1a79253aa427.json (ESPN) and scrape_82fb73e8e332.json (BBC):
  - xG 2.26 and 0.16.
  - Big chances 0 and 5.
  - Shots on goal 2 and 11.
  - Valverde's goal 0.06 xG, listed at right back, and the BBC says he is captain.
  - Güler's goal 0.31, Mbappé's 0.79 (shots_espn.json); Güler's shots total 2.
  - Güler "volleyed in from six yards" (BBC).
  - Güler's pass for Mbappé's third (BBC live entry 25).
  - Madrid 30 points, level with Barcelona, Valencia 9 points and 19th.
  - "Only goal difference keeps Real off top spot" (BBC), and Madrid are second in the ESPN table.
- Club-leaning papers are not used. The best-player pick is labelled "Scout's pick" and no ratings are claimed. There is no streak claim (the source disagreement was avoided).
- Tone is clean. banter is false, so there is no banter. There is no fan_buzz claim, only a question. No trend claims are made, so the missing trends.json is fine.
- Specs: 1080x1920, H.264 + AAC, 34.2 s (max 50), 6 beats (5-8), -14.6 LUFS (about -14), each beat 8 s or shorter.
- Contact sheets (review_a.jpg, review_b.jpg): no overlapping or clipped text, and captions match the cards. The first frame is the hook card showing the 2.26 and 0.16 payoff. The count-up animations (0.04 to 0.06, 0 to 30) settle on the correct values.
