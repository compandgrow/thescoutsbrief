# Chelsea 1-4 Leeds United, English Premier League, 2026-11-21, Stamford Bridge (London)
Goals (ESPN): Emmanuel Emegha 25' (CHE); Noah Okafor 28', 58' (LEE); Dominic Calvert-Lewin 53' pen (LEE); Brenden Aaronson 90'+1' (LEE, assist Harry Wilson).
Rival (Chelsea) lost at home to an unwatched club: banter true, banter_by_favourite false, favourite_lost false (data/queue.json).
Web path (no PITCHAPI_API_KEY; api.pitchapi.dev did not answer). NO player ratings on this path (BBC page has a fan rater only, no values): label best/worst as "Scout's pick".
Managers (BBC lineups): Chelsea Xabi Alonso, Leeds Daniel Farke. Referee Michael Oliver, VAR Michael Salisbury (BBC Match Officials).
Formations (ESPN + BBC): Chelsea 4-2-3-1, Leeds 3-4-2-1. No shape change stated in any source.
Chelsea XI (BBC): Martínez; Acheampong, Fofana, Colwill, Chavarría; Caicedo (c), Lavia; Estêvão, Palmer, Rogers; Emegha.
Chelsea subs (ESPN/BBC): Henderson for Caicedo 22' (ESPN report: Caicedo "forced off ... after landing awkwardly" = injury, do not mock); Neto for Estêvão 64'; Welbeck for Emegha 64'; Gusto for Acheampong 73'; Quenda for Chavarría 73'.
Leeds XI (BBC): Trafford; Muharemović, Elvedi, Justin; Gudmundsson, Tanaka, Ampadu (c), Bogle; Okafor, Longstaff; Calvert-Lewin.
Leeds subs: Aaronson for Okafor 73'; Rodon for Tanaka 86'; Stach for Bogle 86'; Bard for Gudmundsson 90'+1'; Wilson for Longstaff 90'+1'.
Cards (BBC): Lavia 47' (CHE); Gudmundsson 38', Bogle 68', Longstaff 83' (LEE).

## Cached files (data/research/) and what is in them
- scrape_53aaa01ab081.json = ESPN match page https://www.espn.co.uk/football/match/_/gameId/401879236/leeds-united-chelsea (fetched 2026-11-21T17:48:41Z): score, scorers, records after match (CHE 5-1-5 16 pts, LEE 4-5-2 17 pts), formations/lineups/subs, Match Leaders (Rogers 5 shots 1 SOG 0.17 xG; Calvert-Lewin 6 shots 3 SOG 1.38 xG; Colwill 72 acc passes; Ampadu 58; Fofana 19 def. interventions; Justin 12 def. interventions, 5 tackles, 7 duels won; Martínez 4 saves, 8 SOGA, 2.51 xGC; Trafford 2 saves, 3 SOGA, 0.56 xGC), 35-shot map, short Team Stats (xG 0.56 v 2.51, possession 57% v 43%, shots on goal 3 (21%) v 8 (38%), big chances created 0 v 5, corners 3 v 2, accurate passes 466 (87%) v 334 (82%), duels won 50 v 43, saves 4 v 2, fouls 6 v 15), PL table after match (LEE 6th 17 pts, CHE 8th 16 pts), FT commentary summary ("ending a seven-game winless run at Stamford Bridge dating back to 1999").
- scrape_5ffdcfb0c0e7.json = ESPN team stats https://www.espn.com/soccer/team-stats/_/gameId/401879236 (fetched 2026-11-21T17:49:44Z): Shots (14 v 21, on goal 3 v 8, blocked 5 v 4, woodwork 0 v 1, inside box 7 v 13, outside 7 v 8), Attack (big chances created 0 v 5, big chances missed 0 v 4, through balls 1 v 2, touches in opp box 16 v 34, corners 3 v 2), Passes (accurate 466 (87%) v 334 (82%), passes 538 v 407, accurate long balls 16 v 23, accurate crosses 3 v 6).
- scrape_3a0099246e6f.json = BBC live page https://www.bbc.com/sport/football/live/c3dx19jxx15zt (fetched 2026-11-21T17:49:55Z; multi-match live page, Chelsea v Leeds is the match page): BBC report by Bobbie Jackson ("first win at Chelsea since 1999", "Chelsea have now lost five of their past eight" after "losing just one of their opening six games across all competitions under Alonso", boos, "failed to score in three of their past four across all competitions" before this game), Ampadu quotes, pundit quotes, Opta Match Stats (possession 56.7 v 43.3, xG 0.5565 v 2.5094, shots 14 v 21, SOT 3 v 8, touches in opp box 16 v 34, saves 4 v 2, xG open play 0.25 v 0.65, xG set play 0.31 v 1.07, xA 0.37 v 0.94, distance 119.1 v 125.12 km, offsides 2 v 7, tackles 15 v 17), lineups with managers/cards/subs, match momentum by minute, season-so-far (goals 20 v 14 scored, 20 v 9 conceded; points dropped from winning position CHE 8, LEE 5), form guide, PL table (LEE 6th, CHE 8th).
- scrape_2222d3641408.json = ESPN report https://www.espn.co.uk/football/report/_/gameId/401879236 (free local fetch): PA report, "first Premier League win at Stamford Bridge in 27 years", Leeds lost 6-3 there in the Carabao Cup in September, Caicedo forced off ~20' (injury), Acheampong misjudged bounce before the equaliser, Chelsea booed off at half-time and at the end.
- scrape_4252d8bfe73b.json = ESPN commentary https://www.espn.co.uk/football/commentary/_/gameId/401879236 (free local fetch): 70' to FT plus summary; 83' "Leeds have had 10 [second-half shots] to Chelsea's three"; 90'+3' "ends a 10-game winless run for Leeds against Chelsea ... unbeaten in seven home meetings with the Whites since December 1999, winning six".
- shots_espn.json (local): 35 shots (CHE 14, LEE 21), xG/xGOT/minute/situation. Sums 0.57 / 2.53 (rounding); use the header 0.56 / 2.51.
- _web_sources.json (local): the three URLs above.

## Gate
Score: yes. Team stats: yes (ESPN + BBC Opta). Shots: yes (35). Lineups: yes. PASS.

## Caveats for the analyst
- No player ratings. Best/worst = "Scout's pick".
- Goal minutes differ: ESPN 25'/28', BBC text 28'/"three minutes later". Use ESPN minutes or avoid the opener's minute on screen.
- "First win at Stamford Bridge since 1999": BBC + ESPN (report says "27 years"; commentary "seven-game winless run ... dating back to 1999").
- Caicedo left 22' injured: red line, never mock it.
