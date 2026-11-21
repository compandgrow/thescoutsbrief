# Review: fc-cologne-bayern-munich-2026-11-20

## Round 2 (final round, 2 of 2)

**Verdict: PASS**

Re-render reviewed: `out/reel.mp4`, 34.23 s, timing.json duration 34.216 s.

### Round-1 fixes

1. **Beat 3, gorilla covering the stat row: resolved.** The card now has 3 tiles: "1 goals", "1.43 xG" and "2 of 2 shots on target". The frames at 24 s and 27 s show all three labels clear of the head. The bottom-left tile's corner slightly overlaps the top of the head, but no text is covered.
2. **Beat 3, empty rating tile: resolved.** There is no rating tile and no "–". The "SCOUT'S PICK" badge is used.
3. **Beat 4, outro text running into the presenter: resolved.** "MISSING KANE / OR THE TARGET?" ends well above the head at 31 s and 33 s.
4. **Beat 0, hook payoff after 3 s: resolved, with almost no margin.** The new line is "Bayern one on target, Cologne four. Still one-one." I measured it on voice.wav with energy plus spectral centroid and zero-crossing rate:
   - the "Cologne" /k/ burst is at 2.08 s;
   - the "four" /f/ fricative runs 2.48–2.63 s;
   - the "four" vowel runs 2.64–2.98 s and falls under -50 dB at 2.98 s;
   - "Still" starts at 3.22 s.

   The payoff is spoken by 2.98 s, against `hook.payoff_within_s` of 3. The hook is 8 words (max 10). Frame 0 is the full hook card ("BAYERN 1 / COLOGNE 4 / ON TARGET").
5. **Beat lengths and total duration: resolved.**
   - Beat lengths: beat 0 4.68 s, beat 1 7.88 s, beat 2 7.75 s, beat 3 7.62 s and beat 4 3.74 s. All are 8 s or less.
   - Total: 34.2 s, inside the 28–35 s target and the 40 s max.
   - Beat 1 now says whose 72% it is ("Bayern had seventy-two percent of the ball").
6. **Caption milestone line: resolved.** The "first time since at least 2004-05" line has been removed. No trend claim is left in the caption that is not a talking point.

### Round-2 checks

- **Facts:** I re-checked every number on screen, in the voiceover and in the caption against the cached pages.
  - **1 v 4 on target, 72/28 possession, 1.07/1.99 xG:** ESPN match page `scrape_224cd33dfe21.json` ("1.07 Expected Goals 1.99 72% Possession 28% 1 (6%) Shots on Goal 4 (57%)") and ESPN team stats `scrape_fb37c40bdf78.json` ("1Shots on Goal4").
  - **Kane off at 20' for Bischof, ankle injury:** bundesliga.com `scrape_b053688dcbac.json` ("suspected ankle injury", "replaced by Tom Bischof … in the 20th minute") and the ESPN substitutions. Only "ankle injury" is used; the rejected "months out" claim is not.
  - **15 shots and 0.86 xG after Kane went off:** recounted from shots_espn.json (MUN shots from 22' to 80', 15 shots, xG 0.86), which matches derived.json `BAY_from_20`. Bayern's full-match total was 17 shots with 1 on target, which also matches.
  - **Moore 1 goal, 2 shots, both on target, 1.43 xG:** shots_espn.json, shot 2 (Goal, 0.93) and shot 12 (Saved, 0.50); ESPN Match Leaders "M. Moore … 2 SOG, 1.43 xG".
  - **Names:** spelled as in the data (Mikey Moore, Kane, Bischof).
- **Specs:** 1080x1920, H.264 + AAC 44.1 kHz stereo, 34.23 s, 5 beats (5–8 allowed), -14.7 LUFS integrated, 76 spoken words (110 max).
- **Watch:** I read `out/review_a.jpg` and `out/review_b.jpg`, plus single frames at 0, 3, 9, 17, 24, 27, 31 and 33 s.
  - No text is clipped or overlapping, and no card is empty.
  - The captions follow each card's topic.
  - Emotions fit their beats: shocked on the hook, disappointed on proof and story, excited on the player, happy on the outro.
- **Tone and banter:** `result_context.banter` is false (Bayern, a favourite, drew), and there is no banter beat. None of the `banter.red_lines` is crossed:
  - the injury is stated, not mocked;
  - there are no tragedy references and no personal remarks;
  - the criticism is aimed only at the shot numbers.
- **Trends:** trends.json is present and its notes show the Reddit step was tried. The reel makes no claim about what fans think. The Kane storyline is t1 (strong). No claim from `rejected` is used.
- **Caption:**
  - The first line is "Bayern 1 on target, Cologne 4." (6 words) plus the debate question.
  - There are 10 hashtags.
  - Every number matches the sources.

### Notes (not blocking)

- The hook payoff ends at about 2.98 s, only 0.02 s inside the limit. Future hooks should leave more room.
- Frame 0 shows the full hook card, which is the cover. Frames 1–11 then re-animate the headline in, so the card is partly drawn for about 0.35 s. This is a template behaviour and is acceptable.
- On the player card, "1 goals" should be singular ("goal"). This is a template label.

---

## Round 1

**Verdict: FIX**

## Fix list

1. **Beat 3 (player card, Mikey Moore): the gorilla covers the bottom stat row.** At about 27 s the presenter's head sits over the lower stat tiles. The 4th tile shows "1.43" with its "xG" label hidden, so an unlabelled number is on screen. Move the stat grid up, or use 2 rows of 2 that end above the head, or shrink the card, so that all four labels ("goals", "shots", "on target", "xG") can be seen.
2. **Beat 3 (player card): empty rating tile.** The green "RATING" box shows "–" because `rating` is null on the web path, and it reads as an empty card. Hide the rating tile when there is no rating, or swap it for a "SCOUT'S PICK" badge. Do not put a number there, because this match has no rating source.
3. **Beat 4 (outro card): the text runs into the presenter.** The "?" after "TARGET" sits on the gorilla's head (about 34 s). Lower the card `size` or reflow the text (for example "MISSING KANE / OR THE *TARGET*?") so that it ends above the head.
4. **Beat 0 (hook): the payoff finishes after 3 s.** Measured on voice.wav, "Cologne" is spoken at 2.58–3.13 s and "four" at 3.51–3.89 s. The limit in `format.json` → `hook.payoff_within_s` is 3 s. Bayern's "one shot on target" lands at 2.26 s, but the 1-v-4 contrast, which is the hook card, does not. Remove the comma pauses, e.g. `"Bayern one on target, Cologne four. Still one-one."`, and check again that the word "four" ends before 3.0 s.
5. **Beat 2 (stat card) is too long, and so is the reel.** Beat 2 runs 9.38 s, over the `pacing.max_seconds_per_beat` limit of 8 s. Beat 1 runs 8.30 s, also over. The total is 37.2 s against the v3 target of 28–35 s; it is inside the 40 s max, but this is the first v3 test reel. Suggested lines:
   - Beat 2: `"Kane went off injured after twenty minutes. Then: fifteen Bayern shots, nought point eight six expected goals."`
   - Beat 1: `"Bayern had seventy-two percent of the ball. Cologne had more xG: one point nine nine to one point oh seven."`

   Re-render and confirm the total is 35 s or less. Beat 1's current line also never says whose 72% it is, and the rewrite fixes that.
6. **Caption: a milestone that is not a talking point.** The line "ESPN: the first time Bayern had just one shot on target in a Bundesliga home game since at least 2004-05." is verbatim in the cached ESPN story (`data/research/scrape_fe3537c9ce70.json`) and in insights.json `surprise_stat`. However, check 6b requires every milestone or storyline to be a `trends.json` talking point with strength strong or medium, and it is not one. Either remove the line, or have trend-scout add it as a talking point (single trusted outlet, so strength medium at most) before posting.

## Checked and OK

- **Facts:** every number was checked against the cached pages.
  - The hook (1 v 4 on target), possession (72/28) and xG (1.07/1.99) match the ESPN match page Team Stats (`scrape_224cd33dfe21.json`: "1 (6%) Shots on Goal 4 (57%)", "72% Possession 28%", "1.07 Expected Goals 1.99") and the ESPN team-stats page (`scrape_fb37c40bdf78.json`: "1Shots on Goal4", "17Shots7").
  - Kane off at 20' for Bischof with an ankle injury: ESPN substitutions, bundesliga.com (`scrape_b053688dcbac.json`, "suspected ankle injury … replaced by Tom Bischof in the 20th minute") and the ESPN story.
  - 15 shots and 0.86 xG from 20': recounted by hand from shots_espn.json (shots 4–11, 13, 16–21; xG adds up to 0.86), which matches derived.json `BAY_from_20`.
  - Moore 2 shots, 2 on target, 1.43 xG, 1 goal: ESPN Match Leaders "2 SOG, 1.43 xG", and shots 2 (goal, 0.93) and 12 (saved, 0.50).
  - Names are spelled as in the data.
  - The reel says only "ankle injury". It does not use the "months out" claim that trends.json rejected.
- **Specs:** 1080x1920, H.264 + AAC 44.1 kHz stereo, 37.23 s (40 s max), 5 beats (5–8 allowed), -14.7 LUFS integrated, 83 spoken words (110 max).
- **First frame:** the hook card shows "BAYERN 1 / COLOGNE 4 / ON TARGET" in big text from frame 0, and the cover is not blank.
- **Structure:** hook → compare (proof) → stat (story, t1) → player → outro. The debate question is 7 words, and the caption opens with the hook and the question.
- **Tone and banter:** `result_context.banter` is false (Bayern, a favourite, drew), and there is no banter beat, which is correct. None of the red lines in `config/teams.json` → `banter.red_lines` is crossed:
  - Kane's injury is stated, not mocked.
  - There is no tragedy reference or personal comment.
  - The criticism is aimed only at the shot numbers.
- **Trends:** trends.json exists, and the notes show the Reddit step was tried (RSS 404, no keys). The reel makes no claim about what fans think. The Kane storyline is t1 (strong).
- **Caption:** caption.txt exists and has 10 hashtags (6–10 allowed). Apart from item 6, its numbers match the sources.
- **Sheets:** `out/review_a.jpg` and `out/review_b.jpg`, plus single frames at 0, 12.5, 27 and 34 s.
