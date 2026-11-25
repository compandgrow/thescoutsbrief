# Review: psv-eindhoven-real-madrid-2026-11-24 (round 2)

**Verdict: PASS**

Round 1 was FIX: the hook payoff came after 3 s, and "Huijsen" was hidden behind the presenter on beat 1. Both are fixed in the re-render (`out/reel.mp4`, 00:11). I re-checked the reel from scratch.

## Round 1 fixes

1. **Beat 0 (hook): fixed.** The line is now "Won five-one. Out-shot eight to four at half-time." (8 words). I checked it against `audio/voice.wav` with a 50 ms energy envelope and silencedetect at -30 dB / 40 ms:

   | Words | Spoken (s) |
   | --- | --- |
   | "Won five-one." | 0.06–1.17 |
   | "Out-shot" | 1.33–1.83 |
   | "eight" | 1.98–2.11 |
   | "to" | 2.23–2.35 |
   | "four" | 2.48–2.77 |
   | "at half-time" | 2.84–3.53 |

   - The paradox (the 5-1 win) lands at 1.17 s, in 3 words.
   - The surprising number (8 to 4) lands at 2.77 s, in 6 words.
   - Both are inside `hook.payoff_within_s: 3` and `hook.max_words: 10`.
   - The trailing "at half-time" runs to 3.53 s. It is context, not payoff.
   - Frame 0 is still the hook card, not blank: "REAL MADRID 5–1 PSV" above "HALF-TIME SHOTS / PSV 8 / MADRID 4" in big text. It agrees with the new line.
   - The line has no named subject, but the card kicker and the score pill on screen make clear that Madrid won and were out-shot.

2. **Beat 1 (stat card): fixed.** The kicker now reads "ON AT 46': BELLINGHAM · HUIJSEN · KONATÉ" and `sub` is removed.
   - A full-size frame at 9 s shows all three names in full on one line. Nothing overlaps the presenter or runs past the right margin.
   - "1ST HALF 0 · 2ND HALF 9" sits well above the presenter's head.
   - Contact-sheet frames from 3.9 s to 11.6 s show the same layout throughout the beat.

## Full re-check

- **Facts.** The numbers are unchanged from round 1, which I verified against the raw files:
  - Half-time shots 8 v 4, and Madrid shots on target 0 then 9, from `shots_espn.json` shot by shot. ESPN and BBC both give 9 v 1 for the full match.
  - Subs at 46' from the BBC line-ups.
  - Bellingham 1 goal, 1 assist, 3 shots from ESPN player stats. His 60' goal had 0.03 xG and made it 2-1 (ESPN shot 19 of 34).
  - Mbappé 2 goals, 1 assist, 9 shots from ESPN player stats.
  - 5 wins from 5, 15 points and first place from the ESPN table and BBC.
  - The new hook text adds no new number: 5-1 and 8 v 4 are both already verified.
- **Contact sheets.** I regenerated `out/review_a.jpg` and `out/review_b.jpg` from the new render and read them.
  - Captions are in sync with the cards.
  - Emotions fit each beat: shocked on the hook, excited on beat 1 and the Scout's pick, neutral with a smug moment on the question, happy on the table and the outro.
  - No clipped text and no empty cards. Partial cards only appear during entry animations: the "12"/"2"/"14" frames are the points counting up to 15, and the compare box fills in.
  - The caption bar is empty only in the final ~1.2 s after the last word (33.5–34.8 s).
  - The outro caption "BELLINGHAM OR MBAPPÉ: WHO / WON THIS ONE?" matches the card.
- **Timing and structure.**
  - 6 beats; the longest is 7.86 s, under the 8 s maximum.
  - Total 34.77 s, now inside the 28–35 s target.
  - Beat 1 leads with the reason for the turnaround (the triple change), as format v4 asks.
  - The outro question is 7 words.
- **Specs.** 1080x1920, H.264 30 fps, AAC 44.1 kHz stereo, -14.8 LUFS integrated, peak -1.0 dBFS.
- **Tone and banter.** The favourite won and PSV is not a watched club, so the reel correctly has no banter. No red lines are crossed.
- **Trends.** `trends.json` records the Reddit attempt (RSS 404 on both the match and club calls). The reel makes no fan-opinion claims and uses none of the rejected claims. The table claim is talking point t1, rated strong.
- **Caption.** Unchanged and still consistent with the reel. Every number is supported, there are 10 hashtags, and the debate question is in the first line and again at the end.

## Notes (not blocking)

- In the cached table PSG had played one game fewer (4 GP, 12 pts). "Top of the table" is true as of the source.
- This is the first v4 reel. The beat-1 number (shots on target 0 → 9) is close to the hook's shot count. Watch beat-1 retention when the performance analyst judges v4.
