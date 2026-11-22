PASS

Reviewer, 2026-11-22, round 1: Liverpool 4-0 Man United (reels/manchester-united-liverpool-2026-11-22)

1. Facts (I opened the raw and cached files myself)
- Hook, big chances 7 v 0: data/research/scrape_da15b643b3e0.json (ESPN team stats) has "7Big Chances Created0" under the LIV/MAN header. Matches insights.json team_story.
- Red card at 8': scrape_b0f3ea25478b.json (BBC) has "L. Yoro 8', Red Card at 8 minutes" and "fouled Alexander Isak just outside the box. Dominik Szoboszlai stepped up to send the free-kick...". In shots_espn.json the goals are Szoboszlai 10' and Wirtz 13', so "2-0 by 13'" is correct.
- Shots before and after the red: I recounted shots_espn.json (38 shots). Before the red (0-8'): LIV 3, MAN 1. After it: LIV 25, MAN 9. This matches derived.json.
- xG 4.38 v 0.63 (caption): ESPN match page header (scrape_3b90fda75a3c.json). BBC has 4.3777 v 0.6309. Touches in the opposition box, 60 v 9: ESPN team stats.
- Wirtz (best player, Scout's pick): scrape_c3f32da84d0c.json row TCH 76, G 1, A 1, xA 1.08, BCC 5. Name spelled as in the data.
- 19th, 1 league win in 11, 8 pts: the ESPN PL table (scrape_3b90fda75a3c.json) puts Manchester United in row 19 with 11 played, 1-5-5, -9, 8 pts. ESPN commentary at FT (scrape_873659298bd4.json) says "just one win from 11 league games, and they are 19th".
- Form: data/form/360.json reads LDWLLL, which recounts to W1 D1 L4 and matches trends t2. The reel itself makes no all-competitions form claim. Its "1 league win in 11" comes from the league table record, not the form file, and it is consistent with that file (no league win in the 4 league games listed there).
- No claim in the reel comes from trends.json "rejected" (earliest red, 1937, Ngumoha record, 34 conceded, chants, De Ligt error, red right or wrong). The red-card verdict stays neutral.

2. Watching the film (review_a.jpg, review_b.jpg, review_f0.jpg, review_t*.jpg)
- Stat cards show the real values "8'" and "19th" in big text, with no NaN. They were rendered with the non-numeric template fix (commit d625999).
- Compare card: rows 3/1 and 25/9 fill in within about 0.5 s of the cut. Player card: 1 / 1 / 5. Outro: the question appears in full.
- No clipped or overlapping text. Captions stay in sync with each card's topic.

3. Hook
- Frame 0 is the cover and shows "BIG CHANCES / LIVERPOOL 7 / UNITED 0" in full.
- The spoken line is 8 words (max 10). "Seven" is said in the first second and the line ends by about 3.5 s (beat 0 ends at 4.32 s). The payoff is on screen from frame 0.

4. Tone
- Nothing personal. The red card is framed as a question, and the Wirtz pick is "through gritted teeth".

5. Banter
- favourite_lost is true and banter is false. The reel has no banter beat, no laughing presenter and no joke. OK.

6. Trends and fan angle
- trends.json exists. fan_buzz.note records the Reddit attempt: RSS 404 on /r/soccer/search, /r/reddevils and /r/LiverpoolFC.
- The reel makes no fan-opinion claim.
- "Pochettino's first game, 19th, one league win in 11" is talking point t1, strength strong.

7. Specs
- 1080x1920, H.264 + AAC, 35.0 s (max 40, target 28-35), 6 beats (5-8), -14.7 LUFS integrated.

8. Caption
- caption.txt exists. Every number in it is verified above. The first line has the hook and the question.

Non-blocking notes (optional, no re-render needed)
a. Beat 2 asks "Red card, or Liverpool?" but the outro and caption ask "Yoro's red card, or United's attack?" A future script could use one wording throughout.
b. Beat 2 has a "smug" emote at 5.4 s in a reel about a favourite's loss. It is mild, but "neutral" or "thinking" would suit the no-banter context better.
