# Review: story-james-trafford-2026-11-16 (Scout Files #3)

## Final verdict: PASS (round 2), see the round-2 section at the end

## Verdict: FIX (round 1)

Three required fixes. The story itself holds up: nearly every fact is confirmed in the cached pages, and nothing from `rejected` or `never` appears. But the cover frame has no headline, one number has only one source, and one burned-in caption reads like a typo.

## Required fixes

1. **Cover (frame 0) has no hook headline.** Frame 0 shows only the kicker "JAMES TRAFFORD · SPAIN 2-3 ENGLAND" and a dimmed subtitle. The "SPAIN: 43 UNBEATEN? OVER." headline only slides in over frames 1-12. The first frame is the Instagram cover, so it must show the payoff.
   - Cause: `templates/match-reel.html` line 157 sets `shots[0].start = max(0, b.start - 0.25)`. Beat 0 starts at 0.05 s, so this is `0`, and the cover test on line 326 (`t < s.start`) is never true at t = 0. On Max Dowman it worked because beat 0 started later.
   - Fix: line 326 → `const cover = s === shots[0] && t < Math.max(s.start, 0.001);`. This affects frame 0 only. Do not delay the voice instead: that would push the spoken "Over" (now 2.60 s) close to the 3 s limit.
   - Then re-render, and check that frame 0 shows the full headline with the word OVER.
2. **Beat 4: "Ninety-second minute" has only one source.** Only ESPN (`scrape_91827422656f`) gives "92nd minute". Sky (`scrape_a147e34e5fb5`) says "double save in stoppage time", BBC (`scrape_a7203468556b`) says "late double save", and Tuchel says "at the very end". The rule is 2 trusted outlets.
   - Change `say` to: "Then Madrid. England down to ten. Stoppage time: a double save. Tuchel? Absolutely brilliant."
   - Change `caption` to: "Then Madrid. England down to ten. Stoppage time: a double save. Tuchel? Absolutely brilliant."
   - Re-voice beat 4 and regenerate `timing.json` and `mouth.json`. The card stays as it is: it has no minute.
3. **Beat 5: burned-in caption reads "THERE'S NO NO 1."** The caption bar is all caps, so "There's no No 1." looks like a stutter or typo. The voice already says "number one", and BBC reports it as "there's no number one" (to ITV).
   - Change `caption` to: "Five England caps. Pickford has 94. Tuchel's verdict? There's no number one."
   - The stat card's sub line (mixed case, Sky's wording) can stay.

## Facts checked against the cached pages (not just story.json)

| Claim (screen / voice / caption) | Where confirmed | Result |
|---|---|---|
| Spain 2-3 England, Madrid | BBC a720 ("3-2 win… in Madrid"), Sky a147, ESPN 9182 | OK |
| Spain 43 unbeaten, run ended | ESPN 9182 ("ended Spain's 43-match unbeaten run"), BBC a720 ("their first loss in 43 matches") | OK (2 outlets, same number) |
| England down to ten | ESPN 9182, Sky a147 (Anderson sent off 63'), BBC ddf9 ("down to 10 men") | OK |
| 92nd minute | ESPN 9182 only | **FIX 2** |
| Double save at the very end / "last save" | Sky a147, BBC a720, ESPN 9182 | OK |
| City academy, almost 8 years | Man City official fc7c ("almost eight years… Academy") | OK (official) |
| Sold to Burnley 2023, deal worth up to £19m | BBC 4c0e ("up to £19m"), Sky 3612 (£19m), City fc7c (2023) | OK |
| Bought back in 2025 for £31m, five-year deal | BBC a720 (£31m, 2025), ESPN 9182 (£31m), City fc7c (five-year deal to 2030) | OK |
| City sign Donnarumma; Pep's "cup goalkeeper" | BBC a720, ESPN 9182 | OK (no timing used, as `rejected` requires) |
| Leeds £45m, summer 2026, their No 1 | BBC a720 (£45m "this summer"), ESPN 9182 (£45m, "undisputed No. 1"); Sky a147 has him playing every week for Leeds | OK |
| "England's most expensive goalkeeper by transfer fee… twice (BBC Sport)" | BBC a720, word for word, credited | OK (BBC's wording, not ESPN's "record fee", as `rejected` requires) |
| Quote "…the double save at the very end. Absolutely brilliant." | Sky a147 and ESPN 9182, word for word (shortened from the start only, with an ellipsis) | OK |
| 5 caps, age 24 | BBC a720, Sky a147, ESPN 9182 | OK |
| Pickford 94 caps, age 32, first choice for almost a decade | BBC a720 ("almost 10 years"), Sky a147 ("a decade"), ESPN 9182 | OK |
| Tuchel: "There's no No 1." | Sky a147 (word for word); BBC a720 ("there's no number one", to ITV) | OK (wording of the burned-in caption: **FIX 3**) |
| England in the Nations League quarter-finals | BBC a720 ("England's Nations League quarter-finals"), Sky a147 (link: "England into quarter-finals") | OK |
| caption.txt | All of its claims are covered by the rows above | OK |

**Rejected / never list:**
- None of the denied players are named. Donnarumma's timing, the mental wellbeing quotes, the World Cup third-choice claim, the "record British fee" wording, the save and xG stats, the Guardiola anecdote and "39 years" are all absent.
- Nothing about private life, health, legal matters or cruelty. The tone is praise. Anderson is not named.

## Hook
- Payoff: "Spain, forty-three unbeaten? Over." Measured from voice.wav with silencedetect: "Spain" 0.05-0.71 s, "forty-three unbeaten?" 0.98-2.42 s, "Over" starts at **2.60 s**. That is within 3 s.
- Beat 0 is 10 words. The card shows the payoff from about 0.25 s, and from frame 0 once fix 1 is in.
- The player's name is on frame 0 only in the small kicker. The spoken hook says "City's former cup goalkeeper", not "Trafford". This is acceptable, but the learnings (low confidence) favour naming him in the hook.

## The producer's question: the caption moves to "LAST SAVE: CITY'S FORMER" while "Over" is still being spoken
Not a blocker.
- Why it happens: the template times the karaoke captions by character count across the beat. It does not use real word timings. "43" is two characters but is spoken as the long "forty-three", so the first caption page runs about 0.3-0.6 s ahead of the voice:
  - "OVER" is highlighted at about 1.8-2.3 s.
  - The page flips at about 2.4 s.
  - The voice says "Over" at 2.60 s.
- Why it is acceptable:
  - The payoff word is on screen before it is heard, both in the caption and in the large hook card that stays up for the whole beat. Sound-off viewers, who are most of Instagram, get the payoff earlier, not later.
  - The lag is under 1 s, and no caption ever shows text from a different beat or topic.
- Optional, not required: weight caption timing by the `say` words, or by real word timestamps, so numbers written as digits don't pull the highlight early.

## Watched (sheets: out/review_a.jpg 0-32 s, out/review_b.jpg 0-44 s, plus 32-45 s and the first 24 frames)
- The 3D frog host (fedora, noir office) is visible in every frame, and its emotions change by beat.
- Card text is readable at phone size. There is no clipping beyond the normal mask animations in and out, and no empty cards.
- The cover is blank: see fix 1.

## Specs
- 1080x1920, H.264 + AAC 44.1 kHz stereo, 30 fps.
- Duration 45.57 s (≤ 60 max, inside the 40-55 target). The learnings experiment asked for about 35 s, with the question by about 20 s; here the question comes at about 39 s. That is advisory, not a gate.
- Integrated loudness -14.7 LUFS. `presenter: frog3d`, `series: scout-files`.
- The outro asks the question "Trafford or Pickford for the quarter-final? Your call." and ends with the follow call.

## After the fixes
After the re-render, the reviewer re-checks:
- frame 0;
- the beat 4 voice and caption;
- the beat 5 caption;
- that "Over" still starts at or before 3.0 s.

---

# Round 2 (re-render, out/reel.mp4 45.63 s)

## Verdict: PASS

All three round-1 fixes are in the rendered MP4. There are no regressions.

## Fixes re-checked in the MP4 (not just in reel.json)
1. **Frame 0 (cover): fixed.** The first decoded frame of out/reel.mp4 shows:
   - the kicker "JAMES TRAFFORD · SPAIN 2-3 ENGLAND";
   - the full headline "SPAIN: 43 UNBEATEN? OVER." with OVER in red;
   - the caption "SPAIN, 43 UNBEATEN? OVER.";
   - the frog host.
2. **Beat 4 "Stoppage time": fixed, and confirmed by ear with a speech recogniser.**
   - Method: offline Whisper (openai/whisper-small.en via transformers) on the MP4's own audio track, 25.2-32.6 s.
   - Transcript: "Then Madrid, England, down to 10, stoppage time, a double-save [Tuchel?], absolutely brilliant." "Tuchel?" was misheard as "two-child" under the music. No "ninety-second" anywhere.
   - Supporting evidence: indextts/jobs.json has the new text, and line_34c594545d03.wav was written at 18:24, after the round-1 review.
   - Burned-in caption reads "…TO TEN. STOPPAGE TIME:" then "A DOUBLE SAVE. TUCHEL?" then "ABSOLUTELY BRILLIANT." The quote card is unchanged.
   - Sources: "stoppage time" is in Sky a147 word for word ("double save in stoppage time"). ESPN 9182 has "92nd minute" (= stoppage time) and BBC a720 has "late double save". That is 2+ outlets.
3. **Beat 5 caption: fixed.** The burned-in caption reads "THERE'S NO NUMBER ONE." Whisper hears "There is no number one." The stat card's sub line keeps Sky's mixed-case wording "There's no No 1.", as allowed in round 1.

## Hook timing
- voice.wav silencedetect: "Spain" 0.05-0.71 s, "forty-three unbeaten?" 0.98-2.42 s, **"Over" starts at 2.60 s** (≤ 3.0 s).
- The MP4 audio lines up with voice.wav (cross-correlation lag 0.00 s).
- Whisper on the MP4's first 6 s: "Spain 43 unbeaten, over last save, City's former Cup goalkeeper."

## Regression pass
- Sheets: out/review_a.jpg (0-32 s, regenerated) and 32-45 s at 2 fps, plus full-res frames at 22.0, 27.6, 29.2 and 37.6 s.
- The frog host is visible in every frame.
- No clipped card or caption text beyond the normal in/out mask animations. No empty cards.
- Every card fact is unchanged from round 1 and still matches the cached sources: 43 unbeaten, 2-3, £31m, £19m, Donnarumma / cup goalkeeper, £45m, the BBC "most expensive… twice" line, the Tuchel quote, 5 caps, 24/32, Pickford 94.
- caption.txt is unchanged.
- Beat 6 outro: question plus follow call.
- Specs:
  - 1080x1920 H.264, 30 fps;
  - AAC 44.1 kHz stereo;
  - duration 45.63 s (≤ 60);
  - 7 beats;
  - integrated loudness -14.8 LUFS;
  - `presenter: frog3d`, `series: scout-files`.
- Non-blocking, carried over: the caption highlight runs about 0.3-0.6 s ahead of the voice on the hook page. Digits are timed by character count.
