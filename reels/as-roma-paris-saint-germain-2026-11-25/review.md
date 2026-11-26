FIX

Reviewer, 2026-11-26, round 1: PSG 2-2 Roma, UCL (reels/as-roma-paris-saint-germain-2026-11-25)

Every fact checks out, the hook passes and the frames are clean. The only failure is pacing: two beats run over `config/format.json` → `tunable.pacing.max_seconds_per_beat` (8 s). Earlier reviews enforced this limit (chelsea-sunderland-2026-11-08: 12.5 s; the round where beats of 9.38 s and 8.30 s were flagged), so it is enforced here too.

## Fixes

1. **Beat 1 runs 8.56 s (timing.json 3.828-12.385), over the 8 s limit.** Cut at least 0.7 s of speech. Suggested line: "The reason? Centre-back Mario Hermoso: five shots, one point two expected goals. More than any PSG player." This drops "Roma's"; the card kicker already reads "ROMA CENTRE-BACK". If that is still over 8 s, also drop "Mario". Keep "more than any PSG player", because that clause is the paradox. Do not change the card.
2. **Beat 2 runs 8.28 s (timing.json 12.705-20.988), over the 8 s limit.** Drop the closing "Who decided it?". The card kicker "DEMBÉLÉ OR VITINHA?" still poses the question on screen at about 13 s, and the outro asks it 8 s later. New line: "Dembélé: on at fifty-nine, scored at sixty-two. Vitinha: ninety accurate passes, then the handball." Keep "accurate", because 90 is accurate passes out of 100 attempted. Saying "ninety passes" alone would be wrong. Move the `smug` emote at 6.6 s so it still falls inside the shorter beat (or remove it).

After both cuts, re-render and check that every beat in timing.json is 8.0 s or less. The total should land at about 31 s, inside the 28-35 s target.

## Checks done

### 1. Facts (I re-opened the cached pages)
- **Hook, big chances 4 v 2.** In scrape_bf60ae511c4b.json (ESPN match page, Team Stats), the line reads "2  Big Chances Created  4" with PSG listed first. scrape_d943eaed8076.json (ESPN team stats, Attack) reads "2Big Chances Created4". Correct.
- **Kicker "PSG 2–2 ROMA · 100% START OVER" (trends.json t1, strong).** search_38d1c30d18f3.json has the BBC highlights description "Roma ends Paris St-Germain's 100% start to the competition". scrape_cb93a1b54c9e.json has the ESPN/PA report line "dropped points for the first time in this season's Champions League". The ESPN table in scrape_bf60ae511c4b.json shows "Paris Saint-Germain | 5 | 4 | 1 | 0 | +15 | 13". The BBC page (scrape_547e4f07d4e1.json) gives "League position, Paris Saint-Germain 2nd" and "Total points, Paris Saint-Germain 13". Correct. The rejected "12-game winning run" is not used anywhere.
- **Hermoso.** ESPN Match Leaders show "M. Hermoso D  2 SOG, 1.20 xG  5" and "M. Hermoso D  3 TKL, 6 DUELW  12" (12 defensive interventions, joint-most with Pacho). In shots_espn.json, shots n=1, 4, 9, 12 and 22 give 0.79 + 0.02 + 0.05 + 0.09 + 0.25 = 1.20 xG from 5 shots, and n=1 is the goal at 5'. PSG's highest xG is Dembélé at 0.88 (n=17, 27, 28: 0.79 + 0.06 + 0.03), and no PSG player had more than 3 shots. That supports "more than any PSG player" and "most shots in the match". The spoken "twelve defensive interventions, six duels won, and the opener" is correct.
- **Dembélé 59' / 62'.** The BBC line-ups read "Ferran TorresO. Dembélé 59', substituted for O. Dembélé at 59 minutes". The ESPN header reads "Ousmane Dembélé - 62' Pen". Correct (t3, strong).
- **Vitinha 90/100 and the handball.** ESPN Match Leaders show "Vitinha M  100 PASS, 0 BCC  90". The BBC live text has "Penalty conceded by Vitinha (Paris Saint Germain) with a handball in the penalty area.", then "VAR Decision: Penalty Roma.", then "Goal! Paris Saint Germain 2, Roma 2. Donyell Malen (Roma) converts the penalty". ESPN has "Donyell Malen - 78' Pen" and shots_espn n=21 is the 78' penalty goal. Correct.
- **Sources.** All facts come from ESPN and BBC. No club-leaning paper is used and no grades are shown. Names are spelled as in the data.

### 2. Watching the film (out/review_a.jpg, out/review_b.jpg, out/review_f0.jpg)
- Frame 0 is the complete hook card ("BIG CHANCES / ROMA 4 / PSG 2", with the kicker and the source line), so it works as the cover.
- Each card matches its spoken line, and the karaoke highlight tracks the words.
- There is no clipped or overlapping text. The only empty moments are the usual ~0.3 s reveal after each cut: the 0.00 to 1.20 count-up, and the player-card stats filling in.
- Beat 2's sub line wraps "2–2" onto its own line. It is readable, so this is not a fix.

### 3. Hook
- In voice.wav (silencedetect at -35 dB), "Roma" runs 0.05-0.49 s, "four" 0.59-0.88 s and "big chances" up to 1.85 s. A 0.45 s pause follows, then "PSG" 2.29-2.99 s and "two" 3.07-3.46 s.
- format.json asks for "the surprising number or verdict" within `payoff_within_s` (3 s), with no build-up. The surprising number (Roma, the underdog with 34% of the ball, made four big chances) is spoken by 0.88 s, and the whole phrase by 1.85 s. This is the same standard used for bayern-munich-lille-2026-11-25 (round 2) and as-roma-manchester-united-2026-11-03, where "Seven" at about 1 s passed although the line ended at 3.8 s.
- The hook is 6 words (max 10). Frame 0 shows the full 4 v 2.
- Pass.

### 4. Tone
- There is no anger beat and nothing personal.
- The disappointed emote on Hermoso out-shooting PSG is aimed at PSG's performance. OK.

### 5. Banter
- result_context.banter is false: a draw, against a club not on the watchlist. The reel has no banter beat and no laughing presenter. OK.

### 6. Trends and fan angle
- trends.json exists, and fan_buzz records the Reddit attempt (both commands returned 404).
- The only trend claims are t1 and t3, both strong.
- The reel makes no fan-opinion claim, nothing comes from `rejected`, and there is no form count.

### 7. Specs
- 1080x1920, H.264 + AAC, 30 fps.
- 33.27 s (target 28-35, max 40).
- 5 beats (5-8 allowed).
- 63 spoken words (max 110).
- -14.8 LUFS integrated.
- Beat lengths are 3.46 / **8.56** / **8.28** / 6.92 / 3.47 s. The two in bold are the fixes above.

### 8. Caption
- caption.txt exists. Its first line is the hook ("Big chances: Roma 4, PSG 2.", 6 words) plus the debate question.
- It has 9 hashtags.
- Every number in it checks out above: 66% possession, 698 v 348 passes, 4 v 2 big chances, 2.69 v 1.78 xG, Hermoso's goal at 5', 5 shots, 1.20 xG and 12 interventions, the 59'/62' Dembélé moments, Vitinha's 90/100 passes, Malen's 78' penalty, and 13 points in 2nd. It makes no unsupported claim.

## Non-blocking notes
a. Beat 3 says "and it hurts" while the presenter is `excited` and smiling. Something like `smug` or a brief `disappointed` on "it hurts" would fit the words better. This is optional.
b. TTS leaves a 0.45 s pause after "big chances". The hook would land tighter as one breath.
