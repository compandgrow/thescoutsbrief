# Review: story-alexander-isak-2026-11-26 (Scout Files #8)

**Verdict: FIX** (round 1)

The story is sound and nearly every fact checks out against the cached pages. Two things block it: a club "quote" that the sources don't actually contain, and the hook payoff landing at 3.1-4.0 s instead of within 3 s. All of the fixes are text or script edits plus a re-render. No research is needed.

## Fixes (required)

1. **Beat 0 (hook card) and caption line 1: "NOT FOR SALE." is in quotation marks, but no cached source has Newcastle saying it.** BBC (scrape_ba92fab37c16) says "Newcastle have maintained publicly that Isak isn't for sale". Guardian (scrape_9f44a996916b) says "Newcastle's position at that time was that Isak was not for sale". Both are paraphrases of the club's position, not quotes. Under 7b, a non-verbatim quote fails.
   - Card `text`: `NOT FOR SALE.\nTHEN A *BRITISH RECORD*.` (no quote marks).
   - `caption.txt` line 1: `Not for sale. Then a British record.` (no quote marks).
   - The spoken line has no quote marks and has two sources, so its wording can stay. Fix 2 still applies.
2. **Beat 0 (hook timing): the payoff is spoken at 3.07-4.0 s, which misses the 3 s rule.** Silencedetect on voice.wav puts "Not for sale," at 0-0.93, "said Newcastle." at 1.06-1.96, "Then a" at 2.43-2.92 and "British record." at 3.07-4.0. Change `say`/`caption` to `Newcastle: not for sale. Then a British record.` or `Not for sale. Then a British record.` In the second case, put Newcastle on the card kicker, e.g. `NEWCASTLE'S LINE, SUMMER 2025 · ALEXANDER ISAK`. Re-check timing.json and voice.wav afterwards: "record" must end by 3.0 s.
3. **Beat 1 (chapter 1 card): the quote is not verbatim.** The card has `AND TRUST IS LOST… THE`, and the ellipsis stands for omitted words where none were omitted. BBC reads "When promises are broken and trust is lost, the relationship can't continue." The Guardian has the same words without the comma. Change it to `"WHEN PROMISES ARE BROKEN\nAND TRUST IS LOST, THE\nRELATIONSHIP *CAN'T CONTINUE*."`
4. **Beat 2 (chapter 2 card): the quote is cut off with a full stop.** The source sentence goes on: "...no commitment has ever been made by a club official that Alex can leave Newcastle United this summer." Mark the cut with an ellipsis: `"NO COMMITMENT HAS\n*EVER* BEEN MADE…"`

## Should fix in the same re-render

5. **Length 42.23 s is over the 30-40 s target (the cap is 45).** Learnings say extra seconds only lower the watch ratio. Cut the filler `And that's not the wild part.` from beat 3 (say + caption) so it starts `Newcastle signed a striker. Liverpool came back.` Together with fix 2 that brings the reel to about 39-40 s.
6. Nit: on the stat card the 125 reads "125 £M" (template unit after the number; the Wirtz reel set the same precedent). This is acceptable, but `unit: "M"` with `kicker` `... · £` or label `£125m British transfer record` would read better. Not blocking.

Known and accepted: the outro card's `sub` is not rendered by the template. The question is on screen and in the voice, so nothing is missing.

## Fact check (cached pages opened by the reviewer)

| Claim (voice / card / caption) | Where confirmed |
|---|---|
| Newcastle's position: not for sale (paraphrase, no quote marks) | BBC ba92fab37c16; Guardian 9f44a996916b |
| British record, £125m, deadline day 1 Sep 2025, six-year contract | BBC c470ab1dacf8; Guardian 9f44a996916b |
| Skipped PFA awards (19 Aug 2025), named in PFA team of the season, Instagram statement | BBC ba92fab37c16; Guardian 795ae5d05be6 (dated Tue 19 Aug 2025) |
| "When promises are broken and trust is lost, the relationship can't continue." | BBC ba92fab37c16; Guardian 795ae5d05be6 (needs fix 3 for the punctuation) |
| "no commitment has ever been made by a club official..." (Newcastle statement, 19 Aug) | BBC ba92fab37c16; Guardian 795ae5d05be6 (needs fix 4 for the cut); also BBC c470ab1dacf8 |
| £110m bid rejected, 1 Aug | Guardian 9f44a996916b ("rejected on 1 August"); BBC ba92fab37c16 ("Nineteen days" before 19 Aug); BBC c470ab1dacf8 ("rejected in August") |
| Newcastle signed Woltemade from Stuttgart, then a higher Liverpool offer | BBC c470ab1dacf8 ("from Stuttgart last week"); Guardian 9f44a996916b (£70m Woltemade; higher offer Sunday night) |
| "I want to create history. I want to win trophies." | BBC c470ab1dacf8; Guardian 9f44a996916b |
| "Not for sale, then. Just not for £110m." (jab) | follows from the £110m rejection and £125m sale above, backed by numbers |
| Wednesday 25 Nov 2026, Club Brugge 0-3 Liverpool, Isak two goals, one a chip | BBC 20c7a248699e ("Wednesday's 3-0 win", "scoring twice", "chipped"); Guardian bcb3b86bbda7 (Wed 25 Nov 2026, "a double", "impudent chip"). 25 Nov 2026 is a Wednesday. |
| Iraola: "...in a great moment right now." | BBC 20c7a248699e ("He is in a great moment right now"); Guardian bcb3b86bbda7 ("Alex is in a great moment right now") |
| "Isak forced it" | Guardian 795ae5d05be6 ("endeavouring to force a move"); story angle |

Nothing from `rejected` is used: no 10-goal tally, no away-game streak, no broken leg, no "greedy" chant, no wages or £130m, no thigh-injury claim, no 21:30 announcement. Nothing from `config/stories.json` → `never` is used either: no private life, health, legal claims, rumours or cruelty. The jabs are at the club's transfer decision and are backed by £110m/£125m, so the banter red lines are respected and there is no swearing.

## Watch (review_a.jpg, review_b.jpg, full-size frames)

- The first frame is the cover. It shows the hook card with the payoff ("BRITISH RECORD") and the 3D frog host, so it is not blank.
- `presenter: frog3d`. Inspector Croak renders (WebGL) in every frame.
- No clipped or overlapping text. Cards match the topic of each spoken line. The stat counters count up from 0 at the start of each beat and settle on 125 and 2.
- The caption bar is empty in the short gaps between beats and in the last ~1 s after the voice ends. This is cosmetic and not blocking.
- The outro has the open debate question ("Right call, or should Newcastle hold firm?") and "Follow for the next Scout File".
- Beat 1 follows the setup rule: a new plain fact in 10 words, with the long quote on the card.

## Specs

1080x1920, H.264 + AAC 44.1 kHz stereo, 30 fps. Duration 42.23 s (at or under the 45 s cap, over the 30-40 target; see fix 5). 7 beats. Integrated loudness -14.8 LUFS (OK).

## Caption

`caption.txt` exists. After fix 1, nothing in it lacks a source. The question is repeated and the hashtags are fine.

---

# Round 2

**Verdict: PASS**

All four required fixes and the cut asked for in round 1 are in reel.json, caption.txt, timing.json and the new out/reel.mp4. Every on-screen fact and quote was checked again against the cached pages. Nothing new was found that needs fixing.

## Round 1 fixes verified

1. **Quote marks on "NOT FOR SALE." are gone.**
   - The hook card `text` is `NOT FOR SALE.\nTHEN A *BRITISH RECORD*.`, and the frame-0 render matches.
   - `caption.txt` line 1 is `Newcastle: not for sale. Then a British record.` with no quote marks.
   - The kicker reads `NEWCASTLE · ALEXANDER ISAK`. As a paraphrase of the club's position it is backed by BBC ba92fab37c16 ("maintained publicly that Isak isn't for sale") and Guardian 9f44a996916b ("Isak was not for sale").
2. **The hook payoff now lands inside 3 s.**
   - `say` is `Not for sale. Then a British record.`: 7 words, within the 10-word limit.
   - timing.json beat 0 runs from 0.05 to 2.991 s.
   - Silencedetect on voice.wav shows speech ends at 2.943 s, with silence until beat 1 starts at 3.32 s. "Record" therefore ends before 3.0 s.
   - Frame 0 (the cover) shows the full hook card with BRITISH RECORD in red. The card then re-animates and is fully back by about 0.4 s.
3. **The chapter 1 quote is now verbatim.** The card reads `"WHEN PROMISES ARE BROKEN / AND TRUST IS LOST, THE / RELATIONSHIP CAN'T CONTINUE."`, which matches BBC ba92fab37c16 exactly. Guardian 795ae5d05be6 has the same words, once with the comma and once without. The frame at 5.5 s is checked: no ellipsis and no clipping.
4. **The chapter 2 cut is marked.** The card reads `"NO COMMITMENT HAS / EVER BEEN MADE…"`, a true prefix of the Newcastle statement in BBC ba92fab37c16 and Guardian 795ae5d05be6. The ellipsis is visible in the frame at 11 s.
5. **The filler line is gone.** "And that's not the wild part." has been removed. Beat 3 opens `Newcastle signed a striker. Liverpool came back.`, and the reel is now 39.5 s against a 30-40 s target.

## Facts re-checked (2 trusted outlets each)

| Claim | Sources |
|---|---|
| £125m British record, deadline day 1 Sep 2025, six-year contract | BBC c470ab1dacf8; Guardian 9f44a996916b |
| £110m bid rejected 1 Aug | Guardian 9f44a996916b ("rejected on 1 August"); BBC c470ab1dacf8; Guardian 795ae5d05be6; BBC ba92fab37c16 |
| Skipped the PFA awards and named in the PFA team of the season; Instagram statement 19 Aug 2025 | BBC ba92fab37c16; Guardian 795ae5d05be6 |
| Newcastle signed Woltemade from Stuttgart, then a higher Liverpool offer | BBC c470ab1dacf8; Guardian 9f44a996916b |
| "I want to create history. I want to win trophies." | BBC c470ab1dacf8; Guardian 9f44a996916b (verbatim) |
| 25 Nov 2026, Club Brugge 0-3 Liverpool, Isak 2 goals, one a chip | BBC 20c7a248699e ("Wednesday's 3-0 win", "scoring twice", "chipped"); Guardian bcb3b86bbda7 (Wed 25 Nov 2026, "a double", "impudent chip", "You see 3-0") |
| Iraola: "…in a great moment right now." | BBC 20c7a248699e ("He is in a great moment right now"); Guardian bcb3b86bbda7 ("Alex is in a great moment right now"). The leading ellipsis correctly marks the cut. |

- Nothing from `rejected` is used: no 10-goal tally, no away streak, no broken leg, no "greedy" chant, no wages or £130m, no injury claim and no 21:30 detail.
- Nothing from `config/stories.json` → `never` is used. The jabs ("Not for sale, then. Just not for a hundred and ten.") target the club's transfer decision and are backed by £110m and £125m. There is no swearing.
- Minor point: "chip" is not written into a story.json fact, but both cached sources confirm it. Not blocking.

## Watch

- Full-size frames were checked at 0, 5.5, 11, 17, 23.5, 29, 35.5 and 39.3 s, along with the first 16 frames, review_a.jpg and review_b.jpg (regenerated). The hook, chapter 1, chapter 2, twist, stat (125 £M), now (2 GOALS) and outro cards all render with no clipped or overlapping text, and the captions match each card.
- The host is `presenter: frog3d` and is visible throughout.
- The outro carries the open question ("Right call, or should Newcastle hold firm?").
- Already accepted in round 1 and still cosmetic only:
  - the empty caption bar in the last ~1 s
  - the "125 £M" unit order
  - the outro card says "hold firm" while the voice says "have held firm"

## Specs

- 1080x1920, H.264 + AAC 44.1 kHz stereo, 30 fps.
- 39.50 s, within the 45 s story cap and the 30-40 s target.
- 7 beats and 88 spoken words.
- Integrated loudness is -14.8 LUFS.
