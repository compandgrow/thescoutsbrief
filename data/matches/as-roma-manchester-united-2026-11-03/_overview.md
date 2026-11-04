# AS Roma 2-3 Man United (home: Manchester United) — UEFA Champions League, league phase, 2026-11-03
Web path (no PitchAPI). espn_id 401915308. Final: Man Utd 3-2 Roma (HT 0-2). Goals: Soule 11', Malen pen 17' (Roma); Fernandes pen 58' (retaken), Cunha 83', 86' (MUN). Cunha sent off 90+1 (second yellow).
Queue flags (data/queue.json): favourite_involved true, winner MUN, banter false, banter_by_favourite false, favourite_lost false. No banter beat (Roma is not a watched rival).
No player ratings from a data provider: tell the analyst to label best/worst as "Scout's pick". BBC offers reporter marks (out of 10) and BBC user averages.

## Cached pages (data/research/, each JSON has `data.markdown`, `key` = URL, `fetched_at`)
| File | URL | What is in it |
|---|---|---|
| scrape_881f32ddbd18.json | https://www.espn.co.uk/football/match/_/gameId/401915308/as-roma-manchester-united | score, goal scorers + minutes, full-time commentary (90'+4 etc.), 22-shot map with xG/xGOT/situation, ESPN team stats (xG 2.72 v 1.53, possession 52/48, shots on goal, big chances, passes, duels) |
| scrape_355530e859b9.json | https://www.espn.com/soccer/team-stats/_/gameId/401915308 | Shots 15 v 7, on goal 6 v 4, blocked 4 v 1, woodwork 1 v 1, inside box 7 v 4, big chances, touches in opposition box 30 v 8, passes, last-5 results tables for both clubs |
| scrape_6349c0a71541.json | https://www.bbc.com/sport/football/live/cmj47pveql18t | match report (Simon Stone), manager/player quotes, "how they rated" marks, BBC user ratings, lineups + formations (MUN 4-2-3-1, ROM 3-4-2-1), subs and cards with minutes, Opta-style Match Stats (xG, shots, touches in box, tackles, clearances), league-phase table |
| search_0daa58f3e58f.json | search "Manchester United v AS Roma BBC Sport" | BBC links/snippets |
| search_9fe13ff5b998.json | search "Manchester United Roma Carrick" (trend scout, 2 credits) | ESPN preview ("10 games in a row without a win"), Guardian, Reuters, manutd.com snippets |
Also: data/matches/<slug>/shots_espn.json (parsed shot map, `shots[]`: n, outcome, player, team MAN/ROMA, minute, xg, xgot, situation); _web_sources.json (source URLs). Ignore scrape_3d82b9746589 / scrape_9d6dd3db09ba (other matches).

## Where each fact lives
- Score, scorers, red card: ESPN match page header and commentary; BBC report.
- Team stats: ESPN match page "Team Stats", ESPN team-stats page; BBC "Match Stats > Basic Stats / In-depth".
- Per-shot xG, half split, per-player xG: shots_espn.json (computed by analysis.py -> derived.json).
- Formations/subs/cards: BBC "Team Lineups" (Baleba -> Tielemans at 51 in lineup but "off 50" in rating text: do not use an exact minute).
- Ratings: BBC "Magnificent Man Utd - how they rated" (reporter marks), BBC "Player of the match" (Cunha, avg 7.72; Dalot lowest 4.55).
- Manager quotes (positional change, half-time): BBC live page, Carrick sections.
- Form: data/form/360.json (Man Utd), data/form/104.json (Roma), ESPN results pages (https://www.espn.co.uk/football/team/results/_/id/360 and /104). 360.json flags a gap 2026-09-20 to 2026-10-10.
- League-phase table (MUN 17th/6 pts, ROM 19th/4 pts): BBC page "UEFA Champions League Table".
- No xG-per-half, possession-per-half or heat-map data exists.
