# Atlético Madrid 0-2 Bayern Munich, UEFA Champions League (league phase, matchday 4), 2026-11-03, Metropolitano
Goals: Lennart Karl 54', Konrad Laimer 74' (both Bayern). Favourite (Bayern) beat watched rival (Atlético): banter true, banter_by_favourite true.
Web path (no PitchAPI, no Reddit counts). NO official player ratings: the only ratings are BBC Sport USER averages (label them "BBC fan rating").
Formations (BBC lineups): Atlético 4-4-2 (Simeone); Bayern 4-2-3-1 (René Maric listed as manager). No shape change in source. Atlético made 3 subs at 59' (Koke for Le Normand, Lee Kang-In for Baena, Lookman for Sørloth); Bayern subs: Brown for Karl 68', Kim Min-Jae for Davies 79', Boey for Laimer 89'. Cards: Kimmich 56', G. Simeone 79', Stanišić 90+1'.

## Cached files (data/research/) and what is in them
- scrape_f9c52b63f756.json = ESPN match page https://www.espn.co.uk/football/match/_/gameId/401915386/bayern-munich-atletico-madrid: score, scorers, full-time report text (Karl steals from hesitant Le Normand, chips Oblak 54'; Kane lofts ball to Laimer, 74'; xG 0.83 v 1.77), commentary, 28-shot map with xG/xGOT/minute/situation, short team stats.
- scrape_bb4f0a8a7bc4.json = ESPN team stats https://www.espn.com/soccer/team-stats/_/gameId/401915386: Shots 9 v 19, Shots on Goal 3 v 5, blocked 2 v 4, woodwork 0 v 1, inside box 6 v 9, outside box 3 v 10, big chances 2 v 3, touches in opp box 28 v 38, passes 449 v 638, accurate passes 363 v 570, recent results table.
- scrape_58a2e4106ebf.json = BBC match page https://www.bbc.com/sport/football/live/cmy0r2lw77r1t (page loaded; ignore the 'edigitalsurvey blocked' banner): report text, Player of the match Kane 8.80, BBC user ratings for both XIs, lineups/formations/subs/cards, Opta-style stats (possession 41.5 v 58.5, xG 0.83 v 1.77, shots 9 v 19, SOT 3 v 5, fouls 13 v 3, final-third passes 74 v 207, tackles 26 v 30...), CL table (Bayern 8th, 8 pts; Atlético 22nd, 4 pts), form guide, live text.
- search_cc41d083e423.json = search 'Atletico Madrid Bayern Munich Champions League' (fcbayern.com live ticker/preview/stats = official club source; BBC).
- data/form/132.json (Bayern) and data/form/1068.json (Atlético): ESPN last 6, computed form (no gaps). NOTE form/1068.json does not yet list tonight's result, so its 6 results are the six BEFORE the match.
- derived.json = output of analysis.py (shot-map splits, player shots, cross-checks).
- shots_espn.json (local): ESPN labels Bayern as 'MUN' (page alt-text bug). MUN = Bayern. ATM = Atlético.

## Caveats the analyst should respect
- BBC report says Neuer faced 'just one shot on target'; BBC and ESPN stats both give Atlético 3 on target and 3 Neuer saves. Do not use the 'one shot' line.
- fcbayern.com live ticker says Atlético had no attempt 'since the deflected strike from Barrios in the 15th minute' (at 49'); the ESPN shot map has Atlético shots at 20' and 25' too. Do not use the ticker's gap; use the shot-map gap (25' to 66').
- BBC says 637 Bayern passes, ESPN says 638. Avoid total passes.
- Best/worst: label as BBC fan rating / Scout's pick.
