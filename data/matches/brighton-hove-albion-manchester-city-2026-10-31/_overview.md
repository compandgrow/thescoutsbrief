# Man City 0-1 Brighton & Hove Albion — Premier League, 2026-10-31 (Etihad Stadium)
ESPN id 401879245. Home: Manchester City (MNC in ESPN shot data). Away: Brighton (BHA). Goal: Yasin Ayari 11' (BHA).
Mode: web path (no PitchAPI). No official player ratings exist: analyst must label best/worst as "Scout's pick".
(BBC page has *fan-submitted* average ratings, not an official rating; do not present as a rating without saying so.)

## Cached sources (all in data/research/, JSON with data.markdown)
- ESPN match page: scrape_459e6423c707.json — https://www.espn.co.uk/football/match/_/gameId/401879245/brighton-hove-albion-manchester-city
  commentary/match summary text, goal (Ayari 11'), "xG 1.92 vs 1.0", 28-shot map with xG/xGOT/situation per shot, PA report headline.
- ESPN team stats: scrape_061cf731eb06.json — https://www.espn.com/soccer/team-stats/_/gameId/401879245
  Team Stats block: xG 1.92/1.00, possession 62/38, shots on goal 6/3, big chances created 4/4, corners 8/2, accurate passes 503 (84%)/280 (77%), duels won 58/48, saves 2/7, fouls 9/13. Also 28-shot map.
- BBC match page: scrape_e619d7c60c58.json — https://www.bbc.com/sport/football/live/c6x2v4k8e0y9t
  (big multi-match live page; the Man City v Brighton parts: match report, Maresca/Hurzeler quotes, Team Lineups (formations 4-3-3 vs 4-2-3-1, subs with minutes, yellow cards), Match Stats (shots 21/7, touches in opp. box 67/9, final-third passes 120/31, crosses 24/7, clearances 14/32, tackles 17/22, offsides, woodwork 2/0, xG open play/set play), Head to Head, fan player ratings.)
- Parsed shot map: shots_espn.json (28 shots; team codes MNC/BHA; minute, xg, xgot, outcome, situation).
- Search for BBC page: search_bf8939b115ab.json

## Facts located
- Score/goal/scorer: ESPN match page header; BBC report ("Nunes' miscued clearance fell for Ayari").
- Team stats: ESPN team-stats + BBC Match Stats (shots 21/7 BBC; ESPN shot map has 28 = 21+7).
- Formations: BBC Team Lineups (MCI 4-3-3, BHA 4-2-3-1). Subs: MCI Cherki 55', O'Reilly 64', Foden 79', Allan 79'; BHA Hadjam 64', Yalcouye 72', Hinshelwood 72', Rutter 84'. Cards: BHA Chema Andres 20', De Cuyper 49', Gross 81' (MCI none).
- Errors: BBC report — Matheus Nunes miscued clearance led to the goal.
- Manager quotes: BBC (Maresca, Hurzeler).
- Streaks in BBC report (note for trend-scout to verify): City's first PL defeat without scoring in 25 league matches; Brighton's first win at City in 17 league visits; City winless v Brighton in 5 league games; City back-to-back league defeats.
## Caveats
- ESPN commentary text says Haaland's "only chance ... blocked by Dunk" while shot map lists several Haaland shots: use the shot map for counts, avoid that phrase.
- ESPN page shows "Man City 7-0-2, 21 PTS" and Brighton "6-1-2, 19 PTS" (pre-/post-match ambiguity); BBC says Brighton are "two points behind City in third": avoid league-table numbers unless verified.
