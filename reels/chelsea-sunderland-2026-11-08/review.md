# Review: chelsea-sunderland-2026-11-08

**Verdict: PASS** (after 1 FIX round; no outstanding fixes)

Round 1 FIX items, all applied:
1. Beat 2 ran 12.5 s, over the 8 s pacing limit. Split into two beats (open-play xG; final-third passes). Now 6 beats at 36.9 s.
2. Player card: name wrapped to 3 lines and the stats overlapped the presenter. Name is now "Le Fée", stats are xG and PL pens, and the empty "-" rating tile is removed.
3. Banter beat: the "FULL TIME L" stamp sat on the presenter's head. Stamp removed.
4. caption.txt first line was 10 words and had no debate question. It is now "Penalty or performance? Chelsea had 69%." (6 words).

Facts checked against cache (all match):
- 69%/31% possession, 0.53/2.55 xG: scrape_4f0775d9a314.json (ESPN) and scrape_c74d96800865.json (BBC).
- Open-play xG 1.38/0.32 (1.3802/0.3161): BBC, scrape_c74d96800865.json.
- Final-third passes 35/148: BBC, scrape_c74d96800865.json.
- Le Fée: penalty xG 0.79 (shots_espn.json and derived.json). Three PL penalties this season: BBC image caption. One shot, one goal: derived.json.
- First league win since August: BBC and ESPN. Table (Chelsea 5th 16 pts, Sunderland 18th 8 pts): BBC.
- Fan angle matches trends.json fan_buzz (penalty/referee theme). No fan is quoted. Trend t1 is medium strength.
- Names are spelled as in the data. No club-leaning papers are used.

Other checks:
- Hook: 10 words, "sixty-nine percent" is spoken within about 2 s, and frame 0 shows 69% / 0.53 xG.
- Tone: aimed at numbers and results only.
- Banter: Chelsea is a rival and lost, so banter is allowed. It is backed by numbers, with the laughing presenter on beat 1 and no red lines hit.
- Specs: 1080x1920, H264 and AAC, 36.9 s (max 50), 6 beats (5 to 8), 72 spoken words (max 110).
- Loudness is -15.0 LUFS, 1 LU under the -14 target. Accepted as "about -14", flagged.
- Minor: the caption (not on screen) says Chelsea "stay fifth". Both BBC and the tables say fifth.
