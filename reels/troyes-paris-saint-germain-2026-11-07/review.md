# Review: troyes-paris-saint-germain-2026-11-07

Verdict: FIX

1. caption.txt, first line: config/format.json sets `debate_question_in_caption_first_line: true`. The first line is the hook ("PSG missed 7 big chances and still won. 🦍"), and the question sits on the last line. Change the first line to a question of 8 words or fewer, e.g. "11 straight wins: PSG dominance or luck? 🦍", and keep the hook sentence in line 2.
2. Beat 4 / caption, "11 straight wins" (rule 6b): there is no `trends.json` for this match and no `talking_points` entry. The claim is not a strong or medium trend entry, and `data/form/160.json` stops at 2026-11-03 with 6 wins, so the run can't be recounted. The wording is verified: `data/research/scrape_6989decc2e26.json` (ESPN match page, PA report) says "extended their winning streak to 11 matches in all competitions" and the headline says "11th straight win". Either run trend-scout and add a `talking_points` entry, or have the user accept the single ESPN/PA sentence. If accepted, keep "in all competitions" in the caption (it is there) and don't claim league-only.
3. Minor, optional: duration is 29.87 s, just under the 30 s target floor (max 50, so it passes).

Verified OK
- Facts, checked against scrape_512f9bdfae4a (ESPN team stats) and scrape_6989decc2e26 (ESPN match page):
  - Big Chances Missed 7 (PSG).
  - Shots on Goal 7 vs 3, and 15 shots.
  - Hit Woodwork 2.
  - Touches In Opposition Box 28 vs 11.
  - xG 1.60 vs 0.69.
  - Konaté 6 saves, 7 SOGA, 1.60 xGC.
  - Zabarnyi 39' header from a corner (xG 0.10, 0.03 at 27', total 0.13, 2 shots).
  - Names are spelled correctly.
  - Zabarnyi is credited as "Scout's pick", not a rating.
- Hook: 9 words (limit 10). Beat 0 starts at 0.45 s and "seven big chances" is spoken within about 2 s. Frame 0 shows the full hook card, so the cover is fine.
- Contact sheets: no clipped text, no empty cards, and emotions fit each beat. Card entry animations show brief partial frames, which is normal.
- Specs: 1080x1920, H.264 + AAC, 29.87 s, 5 beats, -14.8 LUFS, true peak -1.4 dBFS.
- Tone: clean. Banter is correctly absent, since Troyes is not a watched club and PSG won. No fan-buzz claims.
- Caption: 10 hashtags (limit 6-10), no unsupported numbers.
