PASS

# Review: manchester-united-sporting-cp-2026-11-25 (round 2)

Verdict: PASS. The round 1 fix is in, and the hook now meets config/format.json v4. Facts, frames, tone and specs were re-checked on the re-rendered reel and are clean.

## Round 1 fix: hook (beat 0)
- `say` is now "Both Sporting goals started with United's keeper." That is 7 words (max 10), with no build-up before the payoff. audio/indextts/jobs.json shows that this exact text was voiced.
- Timing:
  - timing.json has beat 0 at 0.05 to 3.091 s.
  - In audio/voice.wav (silencedetect, -40 dB), speech ends at 3.06 s, followed by a 0.36 s gap before beat 1.
  - In the film sheet, the subtitle "WITH UNITED'S KEEPER." is up from about 1.5 s, so the payoff words are spoken at about 1.5 to 3.06 s. Only the tail of "keeper" runs past 3.0 s (about 60 ms).
  - This meets `hook.payoff_within_s` = 3 and the round 1 target of "at or before about 3.0 s".
- Frame 0 (the cover) is the hook card: "SPORTING 2–2 MAN UTD" / "BOTH SPORTING GOALS: UNITED'S KEEPER", fully drawn and not blank. The emotion is shocked.

## Verified OK
- **Facts.** These were re-checked in the cached pages and the raw data. Beats 1 to 4 are unchanged from round 1.
  - Hook claim and beat 1:
    - ESPN report scrape_840f5f5b714c: "gift Sporting another" (the saved Suárez penalty, then the conceded one).
    - Guardian scrape_a11766a86fa1: "dropped a high ball" at 2-1 with 10 minutes left.
  - xG 2.46 / 1.07 and the 1.25 sum:
    - 2.46 is in ESPN scrape_ca3883766b8d, and "1.07 to their opponents" is in scrape_7fbbb38fc679.
    - shots_espn.json gives n=5 (33', penalty, xG 0.79) and n=16 (80', xG 0.46). These add up to 1.25, matching derived.json SCP_xg_from_lammens_errors.
    - The figure is labelled "Scout calc".
  - Two United goals ruled out: BBC scrape_fa0b680d039a ("Marciniak had blown") and the ESPN report.
  - Pochettino's first win: ESPN report ("first win in charge"). This is trend t1 (strong).
  - BBC ratings: in scrape_fa0b680d039a, Lammens has "Average Rating: 2.91", and the BBC mark is 3 ("Shocking mistake near the end gifted Sporting a second").
  - Goals prevented: ESPN player stats scrape_6f0cf5a4cb9b, Lammens row GP 0.69.
  - Names are spelled as in the data.
- **Frames.** Checked on review_a.jpg, review_b.jpg (regenerated from the new render) and frame 0.
  - No clipped, overlapping or empty cards.
  - Subtitles follow the card topics.
  - Emotions fit each beat: shocked, then disappointed, then neutral to smug, then disappointed to angry on "errors weren't", then happy.
  - The player card reads +0.69, 3/10, 1 and 2.91.
- **Tone and banter.**
  - Anger is aimed at the errors and backed by numbers. There are no personal insults.
  - The result is a draw and Sporting are not a watched club, so there is correctly no banter beat. No red line is crossed.
- **Trends.**
  - trends.json records the Reddit attempt (RSS 404).
  - The reel makes no fan-opinion claims. The only trend claim is t1 (strong), and nothing from `rejected` is used.
- **Specs.**
  - 1080x1920, H.264 + AAC.
  - 31.53 s (target 28-35, max 40), 5 beats.
  - The longest beat is 7.88 s (max 8).
  - -14.9 LUFS integrated.
  - The spoken word count fell from 74 to 70 (max 110).
- **Caption.** caption.txt exists.
  - The first line is "Both Sporting goals: United's keeper. Or the ref?", which carries the hook and the debate.
  - It has 9 hashtags.
  - All claims are sourced as above.

## Notes (not blocking)
- In the 2 fps sheet, the subtitle "WITH UNITED'S KEEPER." is still showing at about 3.0 s, as the stat card starts counting up (0.00). This is a hand-over of a few frames and the audio is in sync, so it is fine.
- The compare card's "2 ruled out" counts the VAR decision against the referee. This was already noted in round 1. It is framed as a debate question, so it can stay.
