# Review: manchester-city-nottingham-forest-2026-11-07

FIX

Checked and OK:
- Numbers match their sources.
  - 78/22 possession, xG 1.59/1.00, 5 v 4 shots on target and "first home win of the season" are in the ESPN team stats and match page (scrape_9ba84440fd28).
  - 33 v 14 touches in the box is in the BBC stats (scrape_93207ce0d033).
  - Delap: 2 goals from 3 shots, xG 0.06+0.06+0.07 = 0.19, xGOT 0.29+0.45 = 0.74 (shots_espn.json).
  - Six points behind Arsenal: 27 v 21 points (ESPN table).
- "3 goals v 2 in the previous six home league games" is BBC live post 19 (scrape_93207ce0d033), word for word. Sourced.
- "Seven wins then three straight losses": ESPN (scrape_9ba84440fd28: "lost three on the spin in the league after winning their opening seven league games") and BBC (scrape_93207ce0d033, Maresca quote and the Sheffield Wednesday 1904-05 stat) both say it. Two outlets, so not inferred. It is league only, see fix 1.
- Banter beat 1 uses the `laughing` presenter and its joke is backed by a number (78% possession, lost 3-1). No red-line content: no tragedy, no player or family abuse, no injury jokes. City is a rival and lost, so banter is allowed.
- Specs: 1080x1920, H.264 + AAC, 32.97 s, 6 beats. The first frame shows the hook card.
- Caption: no unsupported claims.

Fixes:
1. Hook (beat 0 say, hook card text, caption line 1): the streak is league only. data/form/382.json shows a Carabao Cup win on pens (28 Oct) and a Champions League win (20 Oct) between the league results, so "three straight losses" is wrong across all competitions.
   - Change the say to "Man City: seven league wins, then three straight league defeats."
   - Change the card kicker to "MAN CITY · PREMIER LEAGUE" or the text to "7 LEAGUE WINS. *3* LOSSES."
   - Change the caption to "7 league wins, then 3 straight league losses".
   - The 7 wins cannot be recounted from data/form/382.json, which lists only 6 matches. The claim stands on ESPN plus BBC, so keep both in the beat's `source` ("ESPN match page, BBC Sport").
2. Hook timing: "three straight losses" ends at 4.63 s against `hook.payoff_within_s` = 3. Word-level timing is not in timing.json, so I could not confirm "seven wins" lands by 3 s.
   - Tighten to "Seven league wins, then three straight losses." and re-time.
   - If the spoken payoff is still past 3 s, trim the line further.
3. Trends (6b): trends/2026-11-07.json has no talking_points entry for the MCI streak (`trend_used` is null). The claim is covered by insights.json `surprise_stat` plus two outlets, so this is acceptable. Please add the streak to trends.json if the pipeline requires it.
4. Banter beat: the stamp "FULL TIME L" reads as clipped. Change it to "FULL TIME 3-1" or "FT: LOST".
5. Loudness is -15.1 LUFS against the -14 target. This is minor. Normalise if it is cheap.

Not checked: audio, since I can't hear it.
Contact sheets are at reels/manchester-city-nottingham-forest-2026-11-07/out/review_a.jpg and review_b.jpg.
