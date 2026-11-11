# Review: story-marc-andre-ter-stegen-2026-11-11

**Verdict: PASS** (round 2)

The round-1 fixes were re-checked against the new render (out/reel.mp4, 55.47 s) and the cached Bundesliga.com page (data/research/scrape_a7eca9165b41.json). New sheets: out/review_a.jpg, out/review_b.jpg, out/review_first.jpg, plus a sheet covering 32-55 s.

## Round-1 items
1. **"44 caps" is now dated.**
   - Hook say: "Forty-four caps when Neuer finally stepped away."
   - Hook kicker: "WHEN NEUER QUIT IN 2026".
   - Beat 6 sub: "44 caps when Klopp took over · Klopp's starter for the first game".
   - The page supports these dates. It was written when "Klopp begins his tenure" and announced his first squad, for the September/October break, before any Klopp match. Neuer's "second retirement … following Germany's World Cup exit" came before that, and Germany played no match in between. So 44 was his total both when Neuer quit and when Klopp took over. "Klopp's starter for the first game" is the verbatim quote "will be the goalkeeper who starts the first game".
   - Nothing in the reel now presents 44 as today's total. Beat 6's kicker no longer says "NOW".
2. **The unhedged "frontrunner" is gone.** The beat 6 sub now uses the supported Klopp claim.
3. **Beat 3 is attributed.** The say is "The league's own website says: in many other eras…". The card sub is "“…in many other eras he could easily have over 100 caps to his name” — Bundesliga.com", which matches the source word for word.
4. **Caption line 3 is now verbatim:** "…says that in many other eras he could easily have over 100 caps."
5. **The footer can now be read.** "@thescoutbrief" and "Source: Bundesliga.com" have a dark backing and are readable at phone size. The empty source line on the outro is hidden. I checked the template change in commit 6055aa5: the CSS is scoped to `body.host3d`, and the class is only added inside the `HOSTS_3D[reel.presenter]` branch. Gorilla match reels (the `createPresenter` branch) are unaffected.

## Full checklist
- **Facts and quotes:**
  - Both Klopp quotes are verbatim.
  - Seven Spanish titles and the UEFA Champions League, ex-Gladbach and Barcelona: correct.
  - Age 34, Ajax on loan from Barcelona: correct.
  - "Germany's most experienced goalkeeper at international level": correct.
  - Neuer's second international retirement after the 2026 World Cup exit: correct.
- **`never` list and `rejected` items:** nothing on injuries or fitness, nothing on Neuer's current injury, nothing from `rejected`. Neither keeper is cast as a villain.
- **Host:** `presenter: frog3d`.
- **Hook:** the say is 7 words. "Forty-four caps" is spoken from 0.45 s (timing.json beat 0: 0.45 to 4.265). Frame 0 shows "WHEN NEUER QUIT IN 2026 / ONLY 44 CAPS." with the footer.
- **Outro:** the question plus "Follow for the next Scout File".
- **Frames:** no clipped or overlapping text, no empty cards, and the subtitles match each card's topic.
- **Specs:**
  - 1080x1920, H.264 + AAC 44.1 kHz stereo.
  - 55.47 s, under the stories max of 60 s (just over the 40-55 target range).
  - 8 beats.
  - -14.6 LUFS integrated, true peak -0.5 dBFS.
- **Caption (fixed by the reviewer, text only, not in the video):** line 1 was "44 caps when Neuer quit. One of the world's best keepers." That is 10 words, over story-writer's 8-word limit for line 1. It now reads "Only 44 caps when Neuer quit in 2026." (8 words). This also removes an unattributed paraphrase of Klopp's praise. The rest of the caption is supported by the source and has 9 hashtags.

## Note (not a fix)
- For about 0.25 s after the cover frames, the hook headline drops out and animates back in. This comes from the template's cover logic, not from this reel.
