# Review: paris-saint-germain-villarreal-2026-11-03

PASS

Checked (round 1, after producer layout fixes):
- Facts: 12 v 2 shots on target and 43 v 10 touches in box (ESPN team-stats scrape, raw file opened); 4 goals at 9', 12', 13', 17' and Villarreal 2 shots in first 17 min (derived.json / shots_espn.json); Gulácsi pass leading to Doué's goal (BBC scrape: "calamitous pass out from the back ... Doue, who fired home"); 6 conceded, 6 saves; 6/6 wins from data/form/160.json; 4 from 4 in UCL (ESPN report). Names match data. Best/worst are Scout's picks, not ratings, and are not presented as ratings.
- Hook: payoff ("four in seventeen minutes") in the first words, 10 words, hook card from frame 0.
- Tone: aimed at a play and backed by numbers; no banter (favourite won, banter false).
- Trends: 6/6 = t1 (strong), 4 from 4 = t2 (medium). No rumours, no fan claims.
- Specs: 1080x1920, H.264 + AAC, 30.17 s, 5 beats, about -14.8 LUFS.
- Frames: no clipped text, no empty cards, emotion matches beats, captions readable.
- Caption exists, supported.

Notes (non-blocking):
- "Villarreal had two shots" is true for the first 17 minutes (they finished with 14). The card and line sit directly after "in seventeen minutes", so context is clear; do not reuse this phrase without the time window.
- Voice is the offline Kokoro/Echo fallback (IndexTTS not installed).
