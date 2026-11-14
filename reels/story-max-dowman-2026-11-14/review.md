# Review: story-max-dowman-2026-11-14 (Scout Files #2)

**Verdict: FIX**

Reviewed 2026-11-14 against the cached pages, not only against story.json:
- `data/research/scrape_f9faf116e306.json`: arsenal.com, "Timber scores first Netherlands goals", 14 Nov 2026
- `data/research/scrape_08224e024ebd.json`: arsenal.com, "Nine young Gunners called up", 10 Nov 2026
- `data/research/scrape_b7a96d5ded88.json`: arsenal.com player profile
- `data/research/scrape_a36a28f087a2.json`: arsenal.com, "Dowman becomes youngest Champions League player", 05 Nov 2025
- `data/research/search_9d86c613df63.json`: search snippet only, for the rejected claim

## Fixes

1. **Beat 5 (Chapter 3, Everton): the link to the record is not in any cached source.** The profile page lists two separate facts. First, he "is the youngest goalscorer ... in Premier League history". Second, his "most iconic moment" was against Everton: an assist for Gyokeres, then a solo goal voted Goal of the Season. No cached page says that the Everton goal was the one that set the record. The search snippet mentions Everton only because James Vaughan "scored for Everton". The voiceover says "Against Everton: an assist, then a solo goal. Youngest scorer in Premier League history." This, together with the card sub, tells viewers that the Everton goal was the record goal. story.json's twist fact makes the same claim without a source.
   - Change `say` to: "And that's not even the wild part. Against Everton: an assist, then a solo goal. Arsenal's Goal of the Season. He's also the Premier League's youngest ever scorer."
   - Change the card `sub` to: "Arsenal's 2025/26 Goal of the Season · also: youngest PL goalscorer ever".
   - Alternative: scrape `https://www.arsenal.com/news/dowman-becomes-arsenals-and-premier-leagues-youngest-scorer-ag5Xq9P2eIql`. If that page confirms the record goal came against Everton, keep the current wording and add the page as a source.
   - Either way, correct the twist `fact` in story.json.

2. **Beat 3 (Chapter 1, Leeds): "Not his first record" is followed by something that is not a record.** Being the second-youngest Premier League player is a milestone, not a record he took.
   - Change `say` to: "Not his first milestone. Against Leeds: second-youngest player in Premier League history."
   - Or keep "record" and use the real record from the same source (scrape_a36a28f087a2): "Not his first record. Against Brighton: youngest player ever to start for Arsenal's men's team."

3. **Caption, second paragraph.** "And it's not the first record he's taken. Leeds. Slavia Prague. Everton." has the same two problems. Leeds was not a record, and the Everton record link is unverified (fix 1). Change it to: "Before this: second-youngest PL debutant, youngest ever Champions League player, youngest PL scorer and title winner. Case file open."

4. **Beat 1 (hook): the payoff lands after 3 s.** Silence analysis of `audio/voice.wav` shows the timing:
   - Speech starts at 0.46 s.
   - "Sixteen-year-old" runs to 1.80 s.
   - "Max Dowman" runs to 2.32 s, followed by a 0.35 s pause.
   - "Bellingham's record" is spoken from about 3.60 s to 4.70 s.

   That breaks `hook.payoff_within_s: 3` and the stories cold_open rule, "payoff within 3 s". The card does show the payoff from frame 0, and the line is 9 words, so both of those pass. Two ways to fix it:
   - Trim the 0.45 s lead-in silence and the 0.35 s pause after "Dowman", so "Bellingham's" starts at about 2.8 s.
   - Better: rewrite to "Jude Bellingham's record? Gone. Max Dowman is sixteen." This is 8 words and puts the payoff first.

5. **Beat 7 (outro): "One record left" overclaims.** The source (scrape_a36a28f087a2) gives Fati's record as one more target ("that particular record"). It does not say it is the only one left. The same article names another target, Yamal's youngest-starter record.
   - Change `say` to: "Next record in his sights: Ansu Fati's, youngest Champions League scorer. Arsenal say Max has until February twenty twenty-seven. Does he do it? Follow for the next Scout File."
   - In the caption, change "One record still stands" to "Next record in his sights".

After the fixes, re-render and re-check the hook timing in `timing.json` and the voice.

## Checks that passed

**Facts, each checked against the cached page:**
- 16 yrs, 10 months, 13 days; Bellingham 17 yrs, two months, six days, v Kosovo, 2020; came on in a 1-0 defeat against Portugal in Bristol. Source: f9faf116e306 (verbatim).
- Ashton Gate; France on 16 Nov; U16, U17 and U19 before this, so U21 is the "fourth age group". Source: 08224e024ebd.
- Signed 18 May 2015; youngest PL goalscorer and title winner; Everton assist for Gyokeres and solo goal; 2025/26 Goal of the Season. Source: b7a96d5ded88.
- Second-youngest PL player v Leeds in August (2025); 72nd-minute sub; Slavia Prague 0-3 Arsenal (the page says "our 3-0 success in Prague"); youngest ever in the Champions League at 15 yrs 308 days; Moukoko 16 yrs 18 days; Fati 17 yrs 40 days; "until February 2027". Source: a36a28f087a2.
- "Bellingham was seventeen" matches 17y 2m 6d. The "16 YRS" stat card matches his age.

**Sources and rules:**
- All facts come from arsenal.com, which is an official source, so one source per fact is enough.
- No quotes are used. Nothing from `rejected` appears; the date of birth and "16y 73d / James Vaughan" are not used.

**`config/stories.json` → `never`:**
- Nothing about private life, health, legal matters, rumours, cruelty, or "exposed"/"fraud" framing.
- The minor is covered only through his on-pitch records.

**Banter (`config/teams.json` red lines):**
- There is no banter beat and nothing touches a red line.
- Tone is admiring throughout.

**Host and structure:**
- `presenter: frog3d` (Inspector Croak).
- The outro has the open-loop question and "follow for the next Scout File".
- This is correctly numbered #2: ter Stegen was #1 in state.json.

**Video:**
- 1080x1920, H.264 30 fps, AAC 44.1 kHz stereo.
- 52.9 s, inside the stories range (target 40-55, max 60), but well over the reel.json experiment's "about 40 s". Fixes 1 and 5 add a few words, so look for trims elsewhere.
- 7 beats.
- Integrated loudness -14.5 LUFS, LRA 1.9.

**Frames:**
- I read sheets covering the whole running time: `out/review_a.jpg` (0-32 s), `out/review_a2.jpg` (32-53 s) and `out/review_b.jpg`.
- No clipped or overlapping text and no empty cards. Subtitles match the topic on each card.
- Frame 0 is the full hook card, so the cover is good.
- Card emotions fit the beats.

**Caption:**
- `caption.txt` is present. The first line is 7 words, with 9 hashtags.
- The remaining numbers are supported, apart from fixes 3 and 5.

## Advisory (not blocking)

- **Fati's record and the article's age.** The source article is from Nov 2025, so it does not show directly that Fati's record still stands in Nov 2026. The current profile, fetched today, lists his records and includes no Champions League goal, which supports the outro.
- **Empty subtitle bar.** The cover frame and the final second show an empty dark subtitle bar. Hide it when there is no text, if that is easy to do.
