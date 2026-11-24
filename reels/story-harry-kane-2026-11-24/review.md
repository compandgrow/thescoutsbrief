FIX

Reel: story-harry-kane-2026-11-24 (Scout Files #7, Harry Kane). Reviewer round 1.

1. Beat 3 (stat card, 2025-26 Bayern): the "club record" claim has only one outlet. "A club record." (say + caption) and the card label "most by a Bayern player in a season" are backed only by BBC Sport (data/research/scrape_9e593cbe4d28.json: "the most a Bayern player has ever struck in one campaign" / "No player has ever scored so many goals in a season for Bayern"). The other cited pages do not say it: Guardian 17dbab5c6748 (61 for Bayern, 12 for England), ESPN cb7bca64bce4 (73 for club and country), BBC f8287557bd95 (73 in 65) and BBC 4dfd30b6d49a (61 in 51). config/stories.json needs 2 trusted outlets or 1 official source. Fix it one of two ways. (a) Cache a second trusted outlet or an official FC Bayern page that states the record, add it to story.json beat "twist", and add it to the card's source line. (b) Cut the claim: say "And that's not the wild part. Last season, sixty-one goals for Bayern in fifty-one games." and make the card label "in 51 games · *73* for club and country" (or similar), with no record wording. Re-render after either change.

2. Caption (caption.txt, line 2): "Then came four loans, and a season nobody saw coming." The story does not support "nobody saw coming". It also suggests the season came straight after the loans, which were 14 years earlier. Change it to something the story backs, e.g. "Then came four loans. Years later, 61 goals in a season for Bayern." Everything else in the caption is supported.

3. Beat 1 (chapter card) and beat 4 (quote card), readability only: the beige pinned-note prop on the evidence board sits behind the headline. On beat 1 it covers "UM" of "PODIUM"; on beat 4 it covers "WAS" in "THAT PEOPLE THOUGHT WAS". White text on beige loses contrast on a phone. Move the note, or keep it out of the headline area, on text-heavy cards. The text is not clipped, so this alone would not fail the reel. Fix it in the same re-render.

Checks
- 1 Facts: verified in the cached pages, apart from item 1.
  - Ballon d'Or, first Englishman since Michael Owen in 2001: BBC 9e593cbe4d28 (published 26 Oct 2026), BBC 4dfd30b6d49a, and Guardian 157cddf697d3 ("England's 25-year wait").
  - Rejected by Arsenal: BBC 3c5d97d6ff40 and ESPN be1c9708f5e2 (no age used, as story.json `rejected` requires).
  - Inglethorpe quote, verbatim: BBC 3c5d97d6ff40, "He probably wasn't even on the podium."
  - Four loans: BBC 3c5d97d6ff40 ("four loan spells in three seasons") and ESPN be1c9708f5e2.
  - Orient 5 goals in 18: BBC 3c5d97d6ff40 and ESPN be1c9708f5e2.
  - Millwall 9 goals: BBC 3c5d97d6ff40 and ESPN be1c9708f5e2.
  - Norwich and Leicester loans: ESPN be1c9708f5e2 and Guardian 17dbab5c6748.
  - 61 goals in 51 games: BBC 9e593cbe4d28 and BBC 4dfd30b6d49a; 61 goals also in Guardian 17dbab5c6748.
  - 73 for club and country: BBC 9e593cbe4d28 and ESPN cb7bca64bce4.
  - Kane "superstar" quote, told to Dazn: BBC 9e593cbe4d28. The card is a verbatim excerpt; it drops the tail "like some of the guys now", which does not change the meaning.
  - 126 caps, most-capped men's player: BBC f8287557bd95, Guardian 17dbab5c6748, 9a0dc3471432 and dfb5899beaff, and ESPN be1c9708f5e2. 12 Nov 2026 v Croatia is consistent with the Guardian ("Thursday").
  - 156 goals in 161 Bayern games: Guardian a678e02b78f4 and ESPN be1c9708f5e2. The older BBC 3c5d97d6ff40 says 156 in 159; not used.
  - Contract to 2029: Guardian a678e02b78f4 and 9a0dc3471432, and ESPN be1c9708f5e2.
- 2 Watch it: made out/review_a.jpg and out/review_b.jpg and read both. The first frame shows the full hook card (cover OK). No empty cards apart from the 0.3 s gaps between beats. Captions match each card's topic. Only issue: the prop overlap in item 3.
- 3 Hook: PASS. "Rejected by Arsenal, then the Ballon d'Or." is 7 words. In voice.wav, "Ballon d'Or" starts at about 2.33 s and the voice ends at 3.04 s; timing.json gives beat 0 as 0.05-3.087 s. The payoff is spoken within 3 s and is on the first frame.
- 4 Tone: PASS. No insults. Nothing about appearance, family or money ("a bit chubby", the wage and the parents are all left out).
- 7 Specs: PASS. 1080x1920 at 30 fps, H.264 + AAC 44.1 kHz stereo, 39.2 s (series max 45 s, target 30-40 s), 7 beats, -14.8 LUFS integrated (LRA 1.7 LU).
- 7b Scout Files: FIX on item 1 only. presenter is frog3d. I opened 10+ cached source pages. Both quotes are verbatim, with who, when and where. Nothing from `rejected` is used: no age at release, no Brady remark, no fee, no 28-point margin, no Sherwood quote, no FIFPRO snub, no Watford, no wage or family. Nothing from `never`. The outro has the question ("Who got Kane most wrong?") and "Follow for the next Scout File".
- 8 Caption: FIX on item 2 only.
