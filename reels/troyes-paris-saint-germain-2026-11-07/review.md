PASS

# Review: troyes-paris-saint-germain-2026-11-07 (round 2)

Verdict: PASS (round 2: only fix was metadata trend_used/fan_question, applied; no re-render needed)

1. reel.json, metadata only: `trend_used` ("PSG 11 straight wins (all competitions)") and `fan_question` ("Eleven straight wins: PSG dominance or luck?") still carry the removed single-source streak claim. Neither is spoken or shown on a card, but fan_question may be reused as a pinned comment or post text. Change `trend_used` to null (or "none") and `fan_question` to "7 big chances missed: dominance or luck?". No re-render is needed, since these fields are not rendered.

Resolved from round 1
- Caption first line is now a question: "PSG: dominance or luck? 7 big chances missed and still won."
- No streak, run or "straight wins" wording remains in `say`, cards or caption.txt. A grep of reel.json and caption.txt found only the two metadata fields above, plus "eleven" as a touches count in beat 2.
- Rule 6b has nothing left to check: no trend claim is made.

Verified OK
- Facts, checked against scrape_512f9bdfae4a (ESPN team stats): Big Chances Missed 7, Shots on Goal 7 vs 3, 15 shots, Hit Woodwork 2, Touches In Opposition Box 28 vs 11, xG 1.60 vs 0.69. Konaté 6 saves and 1.60 xG faced, and Zabarnyi's 39' header from a corner (xG 0.13, 2 shots), were checked against scrape_6989decc2e26. Names are spelled correctly. Zabarnyi is credited as "Scout's pick", not as a rating.
- Hook: 9 words, with "seven big chances" spoken within about 2 s, and frame 0 shows the hook card.
- Contact sheets were regenerated from the current reel.mp4 and read. Captions are in sync with the cards and the emotions fit each beat. Nothing is empty or clipped. Brief card entry animations show partial frames, which is normal.
- On the player card, the mascot's head slightly overlaps the "minute" label under 39'. The number is readable. This is cosmetic and not a fail.
- Specs: 1080x1920, H.264 + AAC, 5 beats, -14.8 LUFS, true peak -1.4 dBFS.
- Duration is 29.3 s, slightly under the 30 s target floor and within the 50 s max. Noted, not a fail.
- Tone is clean, there is no banter (PSG won, Troyes is not a watched club), and there are no fan-buzz claims.
- Caption: 10 hashtags, no unsupported claims.
