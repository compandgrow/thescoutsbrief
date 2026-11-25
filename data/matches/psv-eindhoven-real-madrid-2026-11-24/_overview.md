# Real Madrid 5-1 PSV Eindhoven, UEFA Champions League (league phase, matchday 5), 2026-11-24 (ESPN 401915298)
Web path (no PitchAPI, no official player ratings). Favourite: Real Madrid (won, home). PSV is not a watched club, so no banter (queue: banter=false, banter_by_favourite=false, favourite_lost=false).
Goals: Perisic 32' pen (PSV), Valverde 50', Bellingham 60', Mbappé 64', 84', Vinícius Júnior 87'. Half-time 0-1.
Formations (ESPN and BBC agree): Real Madrid 4-3-3, PSV 4-4-2. No formation change in either source.
Madrid triple change at half-time: Bellingham for Tchouaméni, Huijsen for Militão, Konaté for Rüdiger (ESPN lists 45', BBC 46'). Later: Camavinga for Güler 70', Díaz for Diomande 80'.
PSV: Bajraktarevic for Perisic at half-time; Fernandez for Wanner 70', Gasiorowski for Kostic 70', Flamingo for Sano 78', Santos for Van Bommel 83'.
Yellow cards (BBC line-ups): Tchouaméni 30', Rüdiger 44', Camavinga 81' (RMA); Kostic 42' (PSV).
Managers: BBC lists João Tralhão (RMA) and Peter Bosz (PSV); ESPN report/story say Mourinho made the half-time changes and quote him. Conflict: do not name Madrid's manager on screen without checking.
ESPN team ids: RMA 86, PSV 148 (from /club/_/id/148/ links on the ESPN match page).

Files (cached pages are JSON with .data.markdown, under data/research/):
- scrape_2c7722c8d458.json  ESPN match page (espn.co.uk, local fetch): score, scorers, formations, lineups/subs with minutes, Match Leaders (Mbappé 9 shots 3 SOG 2.58 xG; Kovár 4 saves, 9 SOGA, 4.79 xGC), ESPN commentary summary + last entries (xG "4.32 compared to PSV's 1.69", Vinícius hit the post twice, Madrid top / PSV into elimination zone), shot map (34 shots, metres), Team Stats block (xG 4.79/1.69, possession 62/38, shots on goal 9/1, big chances 8/3, corners 4/1, accurate passes 571 (90%)/318 (82%), duels won 51/39, saves 0/4, fouls 6/11), UCL table (RMA 5-0-0 15 pts 1st, PSV 1-1-3 4 pts 28th).
- scrape_cbbf3e8318b9.json  ESPN team-stats page (espn.com, Firecrawl): shot map again (yards), Shots block (shots 24/10, blocked 5/2, woodwork 2/0, inside box 19/8, outside 5/2), Attack (big chances 8/3, big chances missed 5/3, touches in opp. box 53/17), Passes (632/388 etc.), RMA last-5 results.
- scrape_95e702bb7ae3.json  BBC general UCL live page (cwly0rk8v8mrt): NOT the match page; only live snippets and the UCL table with form. Low value.
- search_c5496672ddf1.json  search that found the BBC general page; its snippet links the dedicated BBC match page c6zxvne4nk7wt.
- search_925bdd025be7.json  fallback search `"Real Madrid v PSV Eindhoven" --site bbc.com --days 3` (no dedicated match page in results).
- scrape_223bbed96be9.json  BBC match page https://www.bbc.com/sport/football/live/c6zxvne4nk7wt (Firecrawl): line-ups with cards/subs, managers, officials, match momentum table by minute, Opta Match Stats (possession 60.4/39.6, xG 4.3249/1.7534, shots 22/10, on target 9/1, touches in box 50/16, saves 0/4, aerials 8/3, woodwork 2/0, one-on-ones 3/0, offsides 4/0, xG open play 4.27/0.82, xA 2.56/0.70, passes 586/377, pass acc 89.9/81.4, final-third passes 139/62, crosses 2/8, tackles 22/27, won tackle % 63.6/48.1, yellows 3/1), Head-to-head season block, form guide (all competitions), live text page 1 (last ~19 events, incl. assists for goals 4 and 5). Player-rating widget had not closed: no BBC fan ratings.
- scrape_e8fe8d8d8ee5.json  ESPN player stats (espn.co.uk, local fetch): per player TCH, G, A, xG, xA, SOG, SHOT, BCC, DINT, DUELW; keepers GA, SV, SOGA, xGC, xGOTC, GP (goals prevented). Rows are in the order of the player list above each table (forwards, midfielders, defenders).
- data/matches/psv-eindhoven-real-madrid-2026-11-24/shots_espn.json  parsed 34-shot map (n, outcome, player, team, minute, xg, xgot, situation).

Known disagreements between sources (analyst: avoid these exact numbers or pick one and say so):
- Full-match xG: ESPN team stats 4.79/1.69 (= shot-map sum), BBC/Opta 4.32/1.75, ESPN commentary text 4.32/1.69.
- Shots: ESPN 24/10, BBC 22/10. Possession: ESPN 62/38, BBC 60.4/39.6. Shots on target agree (9/1).
Not available: PitchAPI, official player ratings (label best/worst "Scout's pick"), full ESPN commentary (only summary + last entries cached).
