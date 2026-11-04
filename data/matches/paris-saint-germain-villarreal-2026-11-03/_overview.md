# Villarreal 0-6 Paris Saint-Germain — UEFA Champions League, league phase, 3 Nov 2026 (Estadio de la Ceramica)
ESPN id 401915309. Watched club: PSG (favourite, won). Villarreal is not a watched club: no banter. No player ratings exist on the web path: label best/worst "Scout's pick".

Formations (BBC lineups): Villarreal 4-2-3-1 (Iñigo Pérez), PSG 4-3-3 (Luis Enrique). No formation change in the lineups; subs only.

## Cached files (all under data/research/ unless stated)
| Fact | File | Where |
|---|---|---|
| Score, scorers + minutes (Neves 9', Doué 12', Mayulu 13', Ruiz 17' and 50', Boly 78') | scrape_90963676b5f1.json (ESPN match page) | header |
| ESPN match report / commentary text (Gulacsi error, 17-year-old Boly debut, 0.66 xG vs 2.69 xG, joint-biggest margin) | scrape_90963676b5f1.json | markdown, "Match Timeline" |
| Shot map: 36 shots with player, minute, xG, xGOT, situation | data/matches/paris-saint-germain-villarreal-2026-11-03/shots_espn.json (same ESPN page) | shots[] |
| Team stats: xG 0.67 v 2.69, possession 29% v 71%, shots on goal 2 v 12, big chances 0 v 2, corners 4 v 8, passes, duels 31 v 44, saves 6 v 2, fouls 19 v 4 | scrape_90963676b5f1.json (tail "Team Stats") and scrape_3d82b9746589.json (ESPN team stats page) | markdown |
| Shots 14 v 22, blocked 5 v 7, inside box 5 v 18, touches in opposition box 10 v 43, accurate passes 237 (78%) v 677 (91%) | scrape_3d82b9746589.json | "Shots", "Attack", "Passes" |
| Report text (all four first goals from Villarreal sloppiness; Gulacsi pass; Boly 17 years old; 20 goals in first four UCL games; PSG top on 12 points) | scrape_9d6dd3db09ba.json (BBC match page) | report |
| League-phase table (PSG 1st, 4 played, 4 won, 20 GF, 5 GA, 12 pts; Villarreal 29th, 1 win, 3 pts, 8 GF, 14 GA) | scrape_9d6dd3db09ba.json | "Champions League Table" |
| Lineups, subs, cards (BBC) | scrape_9d6dd3db09ba.json | "Team Lineups" |
| Search snippets (ESPN, PSG.FR preview) | search_87c40ea83608.json, search_cd61f7b69648.json | |
| Form (last 6, all competitions) | data/form/160.json (PSG), data/form/102.json (Villarreal) | last[] |

## Not available
Player ratings, per-player passes/duels, BBC Opta stats block (page has no stats table). Derived numbers: run data/matches/<slug>/analysis.py -> derived.json.
