# Review: psv-eindhoven-real-madrid-2026-11-24 (round 1)

**Verdict: FIX**

## Fixes

1. **Beat 0 (hook): the payoff lands after 3 s.** Silence analysis of `audio/voice.wav` (same in `line_11e4e4e3c71f.wav`):
   - "Half-time:" runs 0.05–0.70 s, then a 0.34 s pause.
   - "PSV eight shots," runs 1.04–2.39 s.
   - "Madrid four." runs 2.66–3.55 s, then a 0.64 s pause.
   - "Madrid won five-one." runs 4.19–5.67 s.

   The surprising pair (PSV 8, Madrid 4) only completes at 3.55 s. The paradox that makes it a hook (they still won 5-1) completes at 5.67 s. Both are past `hook.payoff_within_s: 3`. This is the same failure as story-max-dowman-2026-11-14. The line is 9 words and frame 0 shows the payoff, so those two checks pass.
   - Change `say` to: "Out-shot eight to four at half-time. Won five-one." (8 words; leads with the numbers and has no "Half-time:" build-up).
   - Alternative: "PSV out-shot Madrid eight to four. Madrid won five-one." (9 words).
   - Keep the hook card as it is.
   - After re-voicing, cut any pause over 0.3 s inside the line, then confirm from the audio that "five-one" ends by 3.0 s. If it does not, use a shorter line. Do not move to beat 1 until it does.

2. **Beat 1 (stat card, "THE HALF-TIME TRIPLE CHANGE"): the sub line is clipped.** The `sub` "on at 46': Bellingham, Huijsen, Konaté" sits behind the presenter's head for the whole beat. Frames at 11 s, 12 s and 13 s all read "Bellingham, ·ijsen, Konaté": "Huijsen" is hidden, and that line is the reason the beat exists. Pick one:
   - Move the names into the kicker and drop `sub`: `kicker` "ON AT 46': BELLINGHAM · HUIJSEN · KONATÉ", `sub` removed.
   - Or have the producer place the stat card's `sub` above the presenter's head box.

   Re-check a full-resolution frame at about 11 s afterwards. All three names must be fully visible.

After these fixes, re-render. Then re-check timing.json, frame 0 and frame ~11 s, the duration (currently 36.9 s) and loudness.

## Verified OK (round 1)

Raw sources opened: `shots_espn.json` (counted shot by shot), `data/research/scrape_2c7722c8d458.json` (ESPN match page), `scrape_e8fe8d8d8ee5.json` (ESPN player stats), `scrape_223bbed96be9.json` (BBC match page), `data/form/86.json`.

- **Half-time shots PSV 8, Madrid 4.** First-half shots in the shot map:
  - PSV: n1, 2, 3, 6, 7, 8, 10, 12 (n12 at 45'+3).
  - RMA: n4, 5, 9, 11 (n11 at 45'+2).
  - Matches derived.json and insights.json.
- **Madrid shots on target 0, then 9.**
  - First half: no RMA shot was Saved or Goal.
  - Second half: n14, 15, 16, 17, 19, 21, 25, 31, 32.
  - The full-match 9 v 1 agrees with ESPN Team Stats "9 (38%) Shots on Goal 1 (10%)" and BBC "Shots on target Real Madrid 9 PSV 1".
- **Three subs at 46'.** BBC line-ups say "J. Bellingham 46', substituted", "Dean Huijsen 46'" and "I. Konaté 46'". ESPN lists 45'. The card credits BBC Sport line-ups, so 46' is fine.
- **Bellingham: 1 goal, 1 assist, 3 shots.**
  - ESPN player stats midfield row 4: TCH 53, G 1, A 1, xG 0.37, SOG 2, SHOT 3.
  - Shot map has 3 shots: n17, n19, n30.
  - The assist is confirmed by BBC "Assisted by Jude Bellingham" for goal 5 and by ESPN's commentary assist tag.
- **Goal xG 0.03 ("three percent chance") made it 2-1.**
  - ESPN cached shot "19 of 34: J. Bellingham, 60', 0.03 xG, 0.39 xGOT, 24 m".
  - Goal order: Perisic 32' (0-1), Valverde 50' (1-1), Bellingham 60' (2-1).
- **Mbappé: 2 goals, 1 assist, 9 shots.**
  - ESPN player stats forward row 1: TCH 66, G 2, A 1, xG 2.58, SOG 3, SHOT 9.
  - Shot map has 9 shots: n9, 11, 13, 16, 21, 27, 29, 31, 33.
- **Five wins from five, 15 points, top.**
  - ESPN UCL table: "Real Madrid 5 5 0 0 +10 15", the first row.
  - BBC: "Real Madrid, Position 1, Points 15".
  - ESPN commentary: "Real Madrid go top of the Champions League standings".
  - This is talking point t1 (strong) in trends.json. It is a table claim, not a form run. form/86.json (WWWWWW) includes two UCL wins (AEK, PSV) and does not contradict it.
- **Names** are spelled as in the data: Bellingham, Mbappé, Huijsen, Konaté. The best player is labelled "SCOUT'S PICK", with no rating shown.
- **Frame 0** is the hook card: "HALF-TIME SHOTS / PSV 8 / MADRID 4" in big text with the 5-1 kicker. Not blank.
- **Contact sheets** `out/review_a.jpg` and `out/review_b.jpg` were made and read, together with full-resolution frames.
  - Captions are in sync with the cards.
  - The empty compare box at 12 s on sheet b is the card entry animation; it is filled by 14.8 s.
  - No empty cards and no wrong emotions: shocked on the hook, excited on the reason and the pick, happy on the table and the outro.
  - The only defect found is fix 2.
- **Tone and banter.** The favourite won and PSV is not a watched club, so there is no banter, and none is in the reel. No insults, and no red lines crossed.
- **Trends.** trends.json exists, and its `fan_buzz.note` records Reddit RSS 404 on both the match call and the club call. The reel makes no fan-opinion claims. No rejected claims are used (no 4-in-5, no Vinícius first goal, no Mourinho quote, no manager name).
- **Specs.**
  - Video: 1080x1920, H.264 30 fps, with AAC 44.1 kHz stereo audio.
  - Length 36.9 s: inside the 40 s max, but above the 28–35 s target. Note only.
  - 6 beats; the longest is 7.86 s, under the 8 s maximum.
  - About 74 spoken words.
  - Loudness -14.7 LUFS integrated (ebur128).
- **Caption.**
  - Every number is supported by the checks above.
  - The first line has the hook plus the debate question.
  - 10 hashtags, and the question is repeated at the end.
  - The first line is 9 words, one over the guideline, but the hook part alone is 6. Accepted, as in earlier reviews.

## Non-blocking notes

- Beat 1 leads with the reason (the triple change), as v4 requires. Its number, shots on target 0 → 9, is a cousin of the hook's shot count. That is acceptable because it measures the effect of the change rather than re-counting the hook's measure. Still, watch the beat-1 retention for this first v4 reel.
- "Top of the table": PSG had played one game fewer (4 GP, 12 pts) when the table was cached. The claim is true as of the source, and the caption and the say line don't overstate it.
