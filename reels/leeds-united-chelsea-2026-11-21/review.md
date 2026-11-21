FIX

Reel: leeds-united-chelsea-2026-11-21 (Chelsea 1-4 Leeds, banter reel). Reviewer round 1.

## Fixes (numbered, must be done before posting)

1. **Beat 3 (player card): the "saves 4" tile is unreadable.** The presenter's head and the anger steam puffs sit on top of the bottom-right stat tile, so only "4 …es" shows (frames at 20-28 s). The steam also overlaps the "2.58 xGOT faced" tile. Change: move the stat grid up, or drop the 4th stat (saves) so the grid is a single row of 3. In the same card, the acute accent on the "Í" of MARTÍNEZ hits the bottom of the "A" in EMILIANO. Increase the line height of the name or lower the size. Also remove the empty red "– RATING" badge, which looks like an empty card element on a web-path reel with no ratings. Hide the badge when `rating` is "–"/null.
2. **Beat 3 is too long and the reel is over the target length.** Beat 3 runs 9.5 s (18.47-27.96), over `pacing.max_seconds_per_beat` = 8. The total of 38.9 s is inside max 40 but over the v3 target of 28-35 s, and this reel's own `experiment` field says 28-35 s. Change the beat 3 `say` to: "Worst on the pitch: Emiliano Martínez. Four conceded, from two point five eight expected on target." (the card keeps 8 on target faced). Tighten beat 1 too, for example "More ball for Chelsea. xG: nought point five six to two point five one." Re-render and aim for 35 s or less.
3. **Beat 2 + caption: table position needs a time qualifier.** trends.json notes say "other games may still move the table on Sunday, so say '8th tonight' rather than final". Brentford (10 GP, 14 pts) can still pass Chelsea. Change the say to "Chelsea drop to eighth tonight, with Leeds above them". Change the card sub to "CHE 8th, 16 pts · LEE 6th, 17 pts (Sat)" or similar. In caption.txt, change "Chelsea drop to 8th on 16 points" to "Chelsea sit 8th tonight on 16 points".

## Verified (opened the cached pages myself)
- Big chances 0 v 5: ESPN team stats (scrape_5ffdcfb0c0e7 "0Big Chances Created5") and ESPN match page Team Stats.
- Possession 56.7 v 43.3 and xG 0.5565 v 2.5094 (0.56 / 2.51): BBC Opta Match Stats (scrape_3a0099246e6f). ESPN 0.56 / 2.51, 57% / 43%.
- "First Leeds win at Stamford Bridge since 1999": chelseafc.com preview "Leeds' last win at the Bridge was in December 1999" (scrape_8d5754179d39). BBC "first win at Chelsea since 1999". ESPN/PA "first Premier League win at Stamford Bridge in 27 years". ESPN commentary "seven-game winless run at Stamford Bridge dating back to 1999". Talking point t1 is strong.
- Table: Chelsea 8th 16 pts, Leeds 6th 17 pts in both the ESPN and BBC tables. BBC: "Chelsea slip to eighth ... Leeds climbing to sixth". Talking point t2 is strong.
- Emiliano Martínez plays for Chelsea: Chelsea starting GK no. 1 in the BBC "home team, Chelsea" lineup, and in the ESPN Chelsea XI (player id 158626 emiliano-martinez). ESPN Match Leaders: 4 saves, 8 SOGA. The spelling matches the data.
- Goals-prevented figure recomputed from the raw ESPN shot map (outcome label precedes each "N of 35"). Leeds' on-target shots are 4 saves (0.05 + 0.04 + 0.09 + 0.57 = 0.75 xGOT) and 4 goals (0.11 + 0.78 pen + 0.91 + 0.03 = 1.83). That gives 8 SOT, 2.58 xGOT, 4 conceded, so 2.58 − 4 = −1.42. This is correct. Only 8 / 4 / 2.58 / 4 are on screen, and those are correct.
- Chelsea's best chance 0.09 xG (Colwill 88'), all 14 shots under 0.10 xG (the 14 values sum to 0.57). Correct.
- Tone/banter: the laughing presenter is on the banter beat, every joke is backed by a number, and Caicedo's injury is not mentioned. No red lines are crossed. No favourite is involved.
- Trend step ran: the Reddit attempt is logged in trends.json notes (RSS 404), and the reel makes no fan-opinion claims.
- Hook: 6 words. "Zero big chances" is spoken by about 2 s and "five" by about 3.3 s. Frame 0 (the cover) shows "BIG CHANCES CHELSEA 0 LEEDS 5". OK.
- Specs: 1080x1920 H.264 + AAC, 30 fps, 38.9 s (max 40), 6 beats (5-8), −14.7 LUFS integrated, 82 spoken words (max 110).
- Caption: hook plus debate question in the first line, 10 hashtags, and every number is sourced (apart from fix 3).
- Contact sheets: out/review_a.jpg and out/review_b.jpg. The other cards are clean. The brief empty frames between cards are transitions only.
