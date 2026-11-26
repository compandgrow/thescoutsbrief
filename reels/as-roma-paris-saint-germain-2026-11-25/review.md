PASS

Reviewer, 2026-11-26, round 2 (final): PSG 2-2 Roma, UCL (reels/as-roma-paris-saint-germain-2026-11-25)

Both round-1 fixes are in the re-render (out/reel.mp4, 00:45). Every beat is now within `tunable.pacing.max_seconds_per_beat` (8 s). I re-checked the whole reel and found nothing to fix.

## Round-1 fixes
1. **Beat 1:** the line is now "The reason? Centre-back Hermoso: five shots, one point two expected goals. More than any PSG player." It runs 7.64 s (timing.json 3.828-11.470). "More than any PSG player" is kept, and the card is unchanged (its kicker still names "ROMA CENTRE-BACK · MARIO HERMOSO"). The emote/slam at 4.6 s falls inside the beat, on "than any PSG player".
2. **Beat 2:** the line is now "Dembélé: on at fifty-nine, scored at sixty-two. Vitinha: ninety accurate passes, then the handball." It runs 7.69 s (11.790-19.480). "Accurate" is kept. The disappointed emote moved to 4.4 s and lands inside the beat, around "ninety accurate passes".

## Checks done

### 1. Facts (I re-opened the cached pages)
- **Hook, 4 v 2.** scrape_bf60ae511c4b.json (ESPN Team Stats, PSG listed first) reads "2 / Big Chances Created / 4". scrape_d943eaed8076.json reads "PSGROMA 2Big Chances Created4". The same block has xG 1.78 v 2.69 and possession 66% v 34%, which matches the caption.
- **Hermoso.** ESPN Match Leaders show "M. Hermoso D 2 SOG, 1.20 xG 5" and "3 TKL, 6 DUELW 12". I recomputed shots_espn.json myself:
  - Hermoso: 5 shots, 1.20 xG.
  - PSG's best is O. Dembélé: 3 shots, 0.88 xG.
  - That supports "more than any PSG player" and the card's "PSG's best: Dembélé 0.88".
- **Dembélé.** BBC line-ups (scrape_547e4f07d4e1.json) read "O. Dembélé 59'". ESPN reads "Ousmane Dembélé - 62' Pen".
- **Vitinha.** ESPN leaders show 90 accurate passes out of 100. The BBC live text reads "Penalty conceded by Vitinha (Paris Saint Germain) with a handball in the penalty area", followed by the VAR decision and Malen's goal at 78'.
- **Kicker "100% START OVER".** BBC (search_38d1c30d18f3.json) reads "100% start to the competition". trends.json t1 is strong.
- **Sources and names.** ESPN and BBC only. No club-leaning paper is used and no grades are shown. Names are spelled as in the data.

### 2. Watching the film (out/review_a.jpg, review_b.jpg, review_f0.jpg)
- Frame 0 is the full hook card (BIG CHANCES / ROMA 4 / PSG 2, with the kicker and the source line), so it works as the cover.
- Each card matches its spoken line, and the karaoke highlight stays in sync through the shortened beats 1-2.
- There is no clipped or overlapping text and no empty card. The only blank moments are the usual ~0.3 s count-up or reveal after each cut.

### 3. Hook
- The voice is unchanged. "Roma four big chances" is spoken by 1.85 s (silencedetect), and "four" lands at about 0.9 s.
- The hook is 6 words (max 10), and frame 0 shows the payoff.
- Pass.

### 4. Tone
- There is no anger beat and nothing personal.
- Beat 3 is now `smug` ("Scout's pick, and it hurts"), which fixes round-1 note a.

### 5. Banter
- result_context.banter is false (a draw), and the reel has no banter beat. OK.

### 6. Trends and fan angle
- trends.json exists, and fan_buzz records the Reddit attempt (404 on both commands).
- The reel uses only t1 and t3 (both strong).
- It makes no fan-opinion claim, uses no form count and uses nothing from `rejected`.

### 7. Specs
- 1080x1920, H.264 + AAC, 30 fps.
- 31.80 s (target 28-35, max 40).
- 5 beats.
- 58 spoken words (max 110).
- -14.9 LUFS integrated.
- Beat lengths are 3.46 / 7.64 / 7.69 / 6.97 / 3.47 s, all 8 s or less.

### 8. Caption
- caption.txt is unchanged and still checks out against the facts above.
- Its first line is the hook plus the debate question.
- It has 9 hashtags and no unsupported claim.

## Non-blocking note
- The 0.45 s TTS pause after "big chances" is still there. It is cosmetic.
