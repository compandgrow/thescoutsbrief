# Liverpool 1-1 Chelsea (Liverpool win 6-5 on pens) - Carabao Cup R4, 28 Oct 2026

espn_id 401921842. Anfield. No extra time: straight to penalties. Goals: Rogers (CHE) 40' pen, Gakpo (LIV) 43' pen. Managers: Iraola (LIV, 4-2-3-1), Alonso (CHE, 4-3-3). Next: LIV v Bournemouth (QF).
Data path: web (no PitchAPI). No player ratings -> best/worst = "Scout's pick".

| Fact | Where (data/research/) |
|---|---|
| Score, goal scorers/minutes, shootout list (8 kicks each, Scored/Missed/Saved), 37-shot map (xG/xGOT/situation/minute), team panel: xG 2.10 v 1.82, possession 52/48, shots on goal 4/4, big chances 2/1, corners 7/5, passes, duels 37/53, saves 3/3, fouls 12/9 | scrape_7e77eb47fd74.json (ESPN match, https://www.espn.co.uk/football/match/_/gameId/401921842/chelsea-liverpool) |
| Shots 10/11, blocked 5/3, inside/outside box, big chances created/missed, touches in box, passes, crosses | scrape_36b60ed9f93d.json (ESPN team stats, https://www.espn.com/soccer/team-stats/_/gameId/401921842) |
| Lineups, formations, subs with minutes, yellow cards, match report (penalty narrative, Wirtz/Barcola 59', Bournemouth next), manager quotes, BBC fan "average rating" (user vote only) | scrape_154a9aff5742.json (BBC, https://www.bbc.com/sport/football/live/c69wz7x4jq71t; has a junk "edigitalsurvey blocked" header, content is real) |
| Parsed shot map (team, player, minute, xG, xGOT, situation, outcome) | data/matches/chelsea-liverpool-2026-10-28/shots_espn.json |
| Derived splits (before/after 59', halves, shootout counts, keeper saves/xGOT) | data/matches/chelsea-liverpool-2026-10-28/derived.json via analysis.py |

Notes for the analyst: shootout kicks in the shot map are minutes 91-104 (situation Penalty); ESPN team-panel xG (2.10) differs slightly from the shot-map sum (2.12). BBC lacks Opta possession/xG tables in this scrape. Tell the scriptwriter: label best/worst "Scout's pick"; banter is light and number-based.
