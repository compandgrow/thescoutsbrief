# Chelsea 2-0 Man Utd — English Premier League, 2026-10-31 (ESPN id 401879248)
Home: Chelsea (CHE, ESPN id 363, manager Xabi Alonso, 4-2-3-1). Away: Manchester United (MUN, ESPN id 360, manager Michael Carrick, 4-2-3-1). Favourite LOST (MUN): no banter.
Goals: M. Rogers 50' (CHE), C. Palmer 64' pen (CHE). L. Martinez (MUN) sent off 63' (second yellow). Rogers 50' / Palmer 64' / Martinez 63' also in ESPN header.

## Cached sources (all under data/research/, JSON key `data.markdown`)
| File | URL | Contains |
|---|---|---|
| scrape_f882629d21b4.json | https://www.espn.co.uk/football/match/_/gameId/401879248/manchester-united-chelsea | score, scorers, 30-shot map with xG/xGOT/distance/situation. Shot 19 (Palmer pen, xG 0.79) shows "No shot data" in the map |
| scrape_f1acb0590062.json | https://www.espn.com/soccer/team-stats/_/gameId/401879248 | shots 18-12, on goal 9-5, blocked 3-3, attempts inside box 13-7, big chances created 2-2, big chances missed 2-3, touches in opposition box 40-21, corners 8-7, passes 542-379 (88% / 77%), last-5 results table for both clubs |
| scrape_641adff637d5.json | https://www.bbc.com/sport/football/live/c6z7xglw0ewzt | match report (Sam Drury), Alonso/Carrick analysis, BBC fan player ratings for all players, lineups, formations, cards and subs with minutes, Opta-style match stats (possession 58.7-41.3, xG 2.6687 vs 1.1654, saves 3-7, fouls 8-20, aerial duels 10-8), match momentum, PL table snapshot |

## Parsed
- data/matches/manchester-united-chelsea-2026-10-31/shots_espn.json: ESPN shot map (29 of 30 shots; n=19 Palmer pen missing; `outcome` labels are NOT reliable, do not use them. xG/minute/player/team are fine). Team labels: CHE, MAN.
- _web_sources.json: the three URLs.

## Notes for the analyst
- No official player ratings. BBC page has **BBC Sport fan (user) average ratings** for every player (Rogers 7.90 best, L. Martinez 2.23 lowest). Label as "BBC fan rating", and in caveats as "Scout's pick"-style transparent source. Not an official rating.
- BBC league table snapshot (17:42) shows MUN 18th, but the BBC report says "leaves United 16th": contradictory, do not use league position.
- BBC report: "without a win in nine games in all competitions, longest such run since October-November 1988" (BBC only; trend-scout to verify).
