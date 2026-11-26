FIX

Reviewer, 2026-11-26, round 1: Lille 2-1 Bayern Munich, UCL (reels/bayern-munich-lille-2026-11-25)

## Fixes (both needed before posting)

1. **Beat 0 (hook): the payoff lands after 3 s.** Measured on audio/voice.wav with silencedetect at -35 dB: "Thirty games unbeaten when one up at half-time." runs from 0.05 to 3.28 s. Then there is 0.97 s of silence (3.28 to 4.25 s), and "Until Lille." runs from 4.25 to 5.12 s. The surprise is that the run ended, and that is "Until Lille", which comes at about 4.3 to 5.1 s. That misses `format.json` → `hook.payoff_within_s` = 3, and also the 4 s that learnings.md allows. "Thirty" on its own is not the payoff, and the near-1 s dead gap inside the hook is build-up. Change `beats[0].say` to a single sentence with no full stop in the middle, so TTS does not pause. Either:
   - `"Thirty games unbeaten one up at half-time, until Lille."` (9 words), or
   - lead with the verdict: `"Lille just ended Bayern's thirty-game half-time unbeaten run."` (8 words). This one needs the card kicker to keep "UCL · ONE UP AT HALF-TIME".

   After you re-voice, check with silencedetect that "Lille" ends before 3.0 s. Keep the card as it is: frame 0 already shows "30 UNBEATEN / THEN LILLE 2-1" in full.

2. **Beats 2, 3 and 5: "Ć" is broken in the display font.** templates/match-reel.html loads only `anton-latin-400-normal.woff2`, which has no Ć. The accent falls back and collides with the C, so the name reads as "PAVLOVIC" with a stray stroke on top. This shows on the player-card name (beat 3, 20-26 s), the outro text (beat 5) and the caption bar (beats 2, 3 and 5). See out/review_zoom_name.jpg and out/review_t35.5.jpg. Preferred fix: add `@font-face` rules for `anton-latin-ext-400-normal.woff2` and `inter-tight-latin-ext-800-normal.woff2` with a latin-ext `unicode-range`. Both files are in node_modules/@fontsource. This is a shared template, so wait until the reel rendering in parallel has finished. Fallback that changes only this reel: write `PAVLOVIC` in `beats[3].card.name` and `beats[5].card.text`, since ESPN spells it that way. The caption bar would still need the template fix. Then re-render and check the name frame again.

After both fixes, re-render and confirm that the duration falls. The fix 1 gap alone saves about 0.8 s.

## Checks done

### 1. Facts (I opened the cached and raw files myself)
- **Hook, "30 unbeaten when one up at half-time"**: confirmed in data/research/scrape_d4068e624f85.json (FC Bayern official live ticker, HT entry). It reads verbatim: "Bayern are unbeaten in 30 Champions League games when they've led by one goal at the break (W28, D2). The last time they lost having been 1-0 up at half-time was in April 2017…". The same page has "Interim result: 0 to 1 after First Half" and a final 2:1, so the HT lead and the defeat are both confirmed. The claim is t1 in trends.json (strength strong, use_for hook), and it is used in the hook together with the score, as learnings.md asks. The stat is Champions League-only. The spoken line leaves that out, but the kicker ("BAYERN · UCL") and the pill show UCL, so this is acceptable.
- **Beat 1, xG from open play 2.06 v 0.25 and from set play 0.05 v 0.93**: BBC match stats in scrape_6edca76f0775.json: "xG from open play Lille 2.0588 Bayern Munich 0.2463" and "xG from set play Lille 0.0528 Bayern Munich 0.9312". Correct. This is the reason behind the hook, not a control measure, so it is v4-compliant.
- **Beat 2, half split xG**: Bayern 1.00 then 0.20, Lille 0.57 then 1.55. Matches derived.json (BAY_1st, BAY_2nd, LIL_1st, LIL_2nd from shots_espn.json, own goal excluded), and the card says the own goal is excluded. The shot-map totals (2.12 / 1.20) differ from the team totals (2.11 / 1.18) by rounding. This is noted in the caveats, and the card does not show totals.
- **Beat 3, Pavlović**: the ESPN player stats in scrape_2bdb88d6d53b.json list Bayern's midfielders in the order Kimmich, Bischof, Pavlovic. Pavlovic's row is TCH 87, xG 0.07, SOG 2, SHOT 2. The own goal at 65' is in the FC Bayern ticker ("Own Goal Pavlović in minute of play 65'") and in the ESPN header ("Aleksandar Pavlovic - 65' OG"). The ESPN report has "clumsily turning the ball into his own net". It was the winning goal, so "decided it" is correct. The card is labelled as Scout's pick (no ratings exist).
- **Beat 4, numbers**: 210 successful final-third passes (Lille 49), box touches 25 v 22 and possession 64.7% are all in the BBC stats (scrape_6edca76f0775.json). The spoken "final-third passes" leaves out "successful", but the card's sub-line says it. Acceptable.
- **Caption**: every number in it (30 / W28 context, 0.25 v 2.06, 0.93 of 1.18, 1.00 then 0.20, 0.57 then 1.55, 65') appears above. No unsupported claims. 10 hashtags (limit 6-10). The debate question is in the first line.

### 2. Watching the film (review_a.jpg, review_b.jpg, review_f0.jpg, review_t*.jpg)
- Frame 0 is the full hook card: "30 UNBEATEN / THEN LILLE 2-1", the kicker, and "Source: FC Bayern official live ticker · ESPN".
- The compare cards fill in within about 0.5 s of each cut. Each card matches its caption. Emotions fit the beats: shocked, then disappointed, angry on the own goal and the rant, and a mild happy outro (same as the PASSed man utd-liverpool loss reel). The only text defect is the Ć glyph (fix 2). Nothing else is clipped or overlapping.

### 3. Hook
- 10 words (max 10). The payoff is late; see fix 1.

### 4. Tone
- The anger is about the own goal and the numbers. Nothing personal. The injury list (Kane, Olise, Neuer) is not used.

### 5. Banter
- result_context: favourite_lost true, banter false. There is no banter beat, no laughing presenter and no joke. OK.

### 6. Trends and fan angle
- trends.json exists. fan_buzz.note records the Reddit attempt (RSS 404 on /r/soccer search and /r/fcbayern). The reel makes no fan-opinion claim; the outro is a question. There are no form claims, and nothing comes from `rejected`.

### 7. Specs
- 1080x1920, H.264 + AAC. Integrated loudness is -14.7 LUFS. 6 beats (5-8). 81 spoken words (max 110). The longest beat is 7.4 s (max 8).
- The duration is 38.13 s. That is within the 40 s max but above the 28-35 s target. Not a fail on its own; fix 1 shortens it. If you want to get closer to 35 s, beat 2's spoken line (19 words) is the longest. You could cut "Bayern's expected goals:" because the card already shows it.

## Non-blocking notes
a. Beat 4's kicker ("64.7% OF THE BALL") and its pass count are control measures. That is fine in the emotion-peak slot, but beat 1 must never move them up.
