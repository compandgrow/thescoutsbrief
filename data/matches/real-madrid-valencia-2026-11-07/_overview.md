# Valencia 0-3 Real Madrid, LaLiga, 2026-11-07 (ESPN 401882808)
Web path (no PitchAPI, no official player ratings). Favourite: Real Madrid (won). Valencia is not a watched club, so no banter.
Goals: Valverde 28', Guler 36', Mbappe 75'. Valencia captain Gaya red card 79' (BBC lineup). Valencia 5-3-2 (Aguirre), Madrid 4-2-3-1 (Mourinho). Madrid subs 84', 84', 84', 90'+1', 90'+1'. Formations did not change in the source.

Files (all under data/research/, JSON with .data.markdown):
- scrape_1a79253aa427.json  ESPN match page: lineups/subs, Match Leaders, Team Stats (xG 0.16/2.26, possession 32/68, shots on goal 2/11, big chances 0/5, corners, passes, duels, saves, fouls), head-to-head, LaLiga table, recap blurb.
- scrape_cc02f6cc3550.json  ESPN team-stats URL (content is the shot map: xG, xGOT, distance, situation per shot).
- scrape_82fb73e8e332.json  BBC live page: report text, live entries (red card, goals), BBC-user average ratings per player (fan ratings, not official), lineups with cards/subs, league table with form.
- data/matches/real-madrid-valencia-2026-11-07/shots_espn.json  parsed 23-shot map (RMA 19 shots, 2.25 xG; VAL 4 shots, 0.16 xG).
Not available: PitchAPI, official ratings, per-player passing/duels, trends.json (trend scout skipped). Label best/worst as "Scout's pick"; BBC ratings are fan averages.
