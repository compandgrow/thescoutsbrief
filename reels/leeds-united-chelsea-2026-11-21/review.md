PASS

Reel: leeds-united-chelsea-2026-11-21 (Chelsea 1-4 Leeds, banter reel). Reviewer round 2. Round 1 was FIX (beat-3 card, length, "8th tonight"); all three fixes are confirmed below.

## Round-1 fixes confirmed
1. Beat 3 player card: a single row of 3 tiles (8 on target faced / 4 conceded / 2.58 xGOT faced), all fully readable at 21.5 s and 23.5 s. The steam puffs sit below the tiles. The MARTÍNEZ accent no longer touches EMILIANO. There is no empty rating badge (the template hides it when the rating is empty, and the `.rating` animation is null-safe).
2. Timing: beats are 3.8 / 5.0 / 7.6 / 7.2 / 4.1 / 4.0 s (all 8 s or less, beat 3 = 7.18 s). The total is 34.53 s, inside the 28-35 s target. There are 71 spoken words.
3. "Eighth tonight" is in the beat 2 say. The card sub is "CHE 8th tonight · LEE 6th", and the caption says "Chelsea sit 8th tonight on 16 points".

## Re-verified independently
- Big chances 0 v 5: ESPN team stats (scrape_5ffdcfb0c0e7, "0Big Chances Created5").
- Possession 56.7 / 43.3 and xG 0.5565 / 2.5094: BBC Opta (scrape_3a0099246e6f).
- 1999: chelseafc.com, "Leeds' last win at the Bridge was in December 1999" (scrape_8d5754179d39). Talking point t1 is strong.
- Table: BBC "Chelsea, Position 8, Points 16" and "Leeds United, Position 6, Points 17", plus "Chelsea slip to eighth ... Leeds climbing to sixth". Talking point t2 is strong, and the trends note on "tonight" is respected.
- Shot map recomputed from shots_espn.json. Chelsea: 14 shots, best 0.09 xG, sum 0.57, all under 0.10. Leeds: 8 on target (saved + goal), 2.58 xGOT, 4 goals. The Martínez card numbers are correct. Martínez is in the Chelsea XI (ESPN id 158626), spelled as in the data.
- Tone/banter: the laughing presenter is on the banter beat, and each joke is backed by a number. No red lines are crossed (no injury, no personal content), and no favourite is involved. The anger on beat 3 is aimed at performance numbers.
- Trend step ran: the Reddit attempt is logged in trends.json notes (RSS 404). There are no fan-opinion claims.
- Hook: 6 words, with the payoff ("Leeds, five") spoken by about 3 s inside beat 0 (0.05-3.87 s). Frame 0 shows "BIG CHANCES / CHELSEA 0 / LEEDS 5" in full.
- Specs: 1080x1920, H.264 + AAC, 30 fps, 34.53 s (max 40), 6 beats (5-8), integrated loudness -14.8 LUFS (LRA 1.6).
- Caption: the hook and the debate question are in the first line, there are 10 hashtags, and every number is sourced.
- Contact sheets were regenerated from the new out/reel.mp4 (out/review_a.jpg, out/review_b.jpg). There is no clipping or overlap and no empty card. The blank-ish frames are transitions only.

## Advisory (not blocking)
- The beat 3 subtitle chunking splits "two point five / eight expected on target", so for about 1 s the subtitle reads "EIGHT EXPECTED ON TARGET." The card shows 2.58 xGOT, so the risk is low. If the subtitles are touched in future, keep number phrases in one chunk.
