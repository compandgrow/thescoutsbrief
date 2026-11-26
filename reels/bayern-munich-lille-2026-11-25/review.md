PASS

Reviewer, 2026-11-26, round 2 (final): Lille 2-1 Bayern Munich, UCL (reels/bayern-munich-lille-2026-11-25)

Both round-1 fixes are done. The reel is ready for the approval step. No fixes are needed.

## Round-1 fixes

1. **Hook timing: passes the written rule.** `config/format.json` → `tunable.hook` has three rules. `payoff_within_s: 3` means the payoff ("the surprising number or verdict", as reviewer.md defines it) must be spoken within 3 s. `max_words: 10` caps the hook length. The `rule` says "Say the surprising number or verdict first, then explain. No build-up before the payoff." Nothing in format.json says the whole hook sentence has to end by 3 s.

   I ran silencedetect at -35 dB on audio/voice.wav and compared it with the caption-bar word highlights at 0.5 s steps in review_a.jpg. The results:
   - 0.05-1.05 s: "Lille just ended".
   - 1.38-1.85 s: "Bayern's".
   - From about 2.0 s: "thirty". The caption bar switches to "THIRTY-GAME…" with THIRTY highlighted at the 2.0 s tile.
   - About 3.5-4.45 s: "unbeaten run".
   - timing.json gives beat 0 as 0.05-4.53 s.

   So the verdict (Lille ended Bayern's run) is spoken by 1.85 s and the surprising number (thirty) by about 2.5 s, both inside 3 s. The sentence opens with the payoff and has no build-up. It is 8 words, under the 10-word cap.

   Frame 0 shows "30 UNBEATEN / THEN LILLE 2-1" with the kicker "BAYERN · UCL · ONE UP AT HALF-TIME". The full meaning is therefore on screen from the first frame, even though the spoken word "unbeaten" only arrives at about 3.5 s.

   For the record, under a stricter reading where the payoff is the whole clause, it would end at 4.45 s and miss 3 s. The format.json wording does not ask for that, and the round-1 fix asked only for "Lille" to land before 3.0 s. It lands at about 0.5 s.

2. **Ć glyph: fixed.** templates/match-reel.html now loads `anton-latin-ext-400-normal.woff2` and `inter-tight-latin-ext-800-normal.woff2` with a latin-ext unicode-range. I checked three places and the Ć renders cleanly in each: the player-card name at 22 s (out/review_t22.jpg), the outro "PAVLOVIĆ / OR THE 2ND HALF?" at 35.5 s (out/review_t35.5.jpg), and the caption bar.

## Checks done

### 1. Facts (I re-opened the cached pages)
- **New hook wording.** data/research/scrape_d4068e624f85.json is the FC Bayern official live ticker. Its HT entry reads verbatim: "Bayern are unbeaten in 30 Champions League games when they've led by one goal at the break (W28, D2). The last time they lost having been 1-0 up at half-time was in April 2017". The same page has "Interim result: 0 to 1 after First Half" and the final 2:1. So Bayern led by one at the break, lost, and Lille ended a 30-game run. "Just ended" is accurate. This is trends.json t1 (strength strong).
  - The spoken "thirty-game half-time unbeaten run" is compressed: it leaves out "Champions League" and "when one up". Out of context it could be heard as "unbeaten at half-time". The frame-0 kicker "BAYERN · UCL · ONE UP AT HALF-TIME" gives the exact condition, and the caption body states it in full ("unbeaten in 30 Champions League games when leading by one goal at the break"). Round 1 set this as the condition for this wording, and it is met. Accepted.
- **Beat 1.** BBC/Opta (scrape_6edca76f0775.json) has open-play xG Lille 2.0588 and Bayern 0.2463, and set-play xG 0.0528 and 0.9312. The card's 2.06 / 0.25 / 0.05 / 0.93 are correct. This is the reason for the result, not a control measure, so it complies with v4.
- **Beat 2.** derived.json gives BAY_1st 1.0, BAY_2nd 0.2, LIL_1st 0.57 and LIL_2nd 1.55. These match the card. The own goal is excluded, and the card says so.
- **Beat 3, Pavlović.** In the ESPN player stats (scrape_2bdb88d6d53b.json), Bayern's midfield rows are Kimmich, Bischof, Pavlovic. The third row reads TCH 87, xG 0.07, SOG 2, SHOT 2. The ESPN header has "Aleksandar Pavlovic - 65' OG" and the FC Bayern ticker has "Own Goal Pavlović in minute of play 65'". It was the winning goal, so "decided it" is correct. The card is labelled as Scout's pick, and the name is spelled as in insights.json.
- **Beat 4.** BBC/Opta has "Successful final third passes Lille 49 Bayern Munich 210", "Total touches inside the opposition box Lille 25 Bayern Munich 22" and "Overall possession … 64.7%". All match.
- **Caption.** It is unchanged from round 1 and every number in it is verified above. It has 10 hashtags. Its first line still reads "30 unbeaten. Until Lille.", which is fine as caption copy.

### 2. Watching the film (review_a.jpg, review_b.jpg, review_f0.jpg, review_t22.jpg, review_t35.5.jpg, plus a sheet of the first 16 frames)
- Frame 0 is the full hook card with the source line, so it works as the cover.
- Each card matches its spoken line, and the karaoke highlight tracks the words.
- The emotions fit: shocked, then disappointed, then angry on the own goal and the rant, then happy at the outro.
- There is no clipped or overlapping text and no empty cards, apart from the normal fill-in for about 0.3 s after each cut.

### 3. Hook
- 8 words (max 10). The payoff is within 3 s, as explained above. Frame 0 shows the payoff.

### 4. Tone
- The anger is aimed at the own goal and the numbers. There is nothing personal, and the injury list is not used.

### 5. Banter
- favourite_lost is true and banter is false. The reel has no banter beat and no laughing presenter. OK.

### 6. Trends and fan angle
- trends.json exists. fan_buzz records the Reddit attempt (unreachable).
- The only trend claim is t1 (strong). The reel makes no fan-opinion claim and no form claim, and uses nothing from `rejected`.

### 7. Specs
- 1080x1920, H.264 + AAC, 30 fps.
- -14.7 LUFS integrated.
- 37.50 s, within the 40 s max.
- 6 beats (5-8 allowed).
- 79 spoken words (max 110).
- Longest beat 7.4 s (beat 2; max 8).

## Non-blocking notes (for learnings, not fixes)
a. The duration of 37.5 s is still above the 28-35 s target. Beat 2's line is the longest. Next time, cutting "Bayern's expected goals:" there would save about 1.5 s.
b. TTS puts a 0.34 s pause after "Lille just ended" (1.05-1.38 s) and another 0.13 s before "unbeaten". The hook would land tighter as one breath.
c. Frame 0 is the complete card. Frames 1-10 then re-run the card's reveal animation, so the hook text briefly empties and redraws (about 0.35 s). This is the template's existing cover behaviour and does not affect the cover or the payoff.
d. Beat 4's kicker and pass count are control measures. That is fine in the emotion-peak slot.
