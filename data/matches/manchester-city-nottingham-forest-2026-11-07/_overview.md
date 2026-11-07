# Nottingham Forest 3-1 Man City — Premier League, 2026-11-07 (City Ground)
ESPN id 401878757. Home: Nottingham Forest (NFO). Away: Manchester City (MNC, watched rival). City LOST -> banter reel (no favourite involved; banter_by_favourite false).
Goals: Jair Cunha 6' (NFO), Liam Delap 18' (NFO), Rayan Cherki 52' (MNC), Liam Delap 73' (NFO).
Mode: web path (no PitchAPI). No official player ratings (BBC page has fan-average ratings only: not used). Best player is "Scout's pick".

## Cached sources (data/research/)
- ESPN match page: scrape_9ba84440fd28.json — https://www.espn.co.uk/football/match/_/gameId/401878757/manchester-city-nottingham-forest (score, scorers, lineups/subs, commentary, 23-shot map, team stats, PL table)
- ESPN team stats: scrape_bd1d193a061f.json — https://www.espn.com/soccer/team-stats/_/gameId/401878757
- BBC live page: scrape_93207ce0d033.json — https://www.bbc.com/sport/football/live/c5wyrmwlv8wvt (report, Match Stats: shots 11/12, touches in box 14/33, xG 1.00/1.59, possession 22/78)
- Parsed shot map: shots_espn.json; halves/player sums: analysis.py
## Facts located
- Possession 22/78, xG 1.00/1.59, shots 11/12, on target 5/4, big chances created 0/3, touches in box 14/33 (ESPN Team Stats, BBC Match Stats).
- ESPN table: City 7-0-3, 21 pts; Arsenal 27 pts (10 played). BBC: City six points behind Arsenal, third league defeat in a row; Forest first home win of season, 16th.
- BBC live post 19: Forest's 3 goals > previous six home league games combined (2).
- BBC report: City conceded eight first-half goals in 10 games; four errors leading to goals.
## Caveats
- ESPN commentary quotes xG 0.98 (Forest) / 1.57 (City): those are Match Leaders goalkeeper xGC values, not team xG. Use 1.00 / 1.59 (team stats, shot-map sums).
- Fan-submitted BBC ratings (Delap 9.02) not official: not used.
- No trends.json (trend-scout skipped, budget); trend facts come from the cached ESPN/BBC pages only.
