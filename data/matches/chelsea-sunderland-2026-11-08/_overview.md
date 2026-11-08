# Sunderland 1-0 Chelsea (Premier League, 8 Nov 2026)

espn_id 401879239, slug chelsea-sunderland, folder `chelsea-sunderland-2026-11-08`. Stadium of Light. Goal: Enzo Le Fée (SUN) 36' penalty. Managers: Régis Le Bris (SUN, 4-2-3-1), Xabi Alonso (CHE, 4-3-2-1). Referee Jarred Gillett.
Data path: web (no PitchAPI). No official player ratings -> best/worst = "Scout's pick". BBC page has a fan-vote "Average rating" (user vote only, not an official rating; do not show as a rating).
Queue: Chelsea is a watched RIVAL that lost -> banter (not by a favourite, no favourite lost).

| Fact | Where (data/research/) |
|---|---|
| Score, goal/minute, formations, subs with minutes, "Match Leaders" (shots, passes, defensive interventions, saves/xGC), PA match report summary, team panel (xG 2.55 v 0.53, possession 31/69, shots on goal 2/4, big chances 2/2, corners 2/2, passes 203 (70%) v 578 (89%), duels 46/49, saves 4/1, fouls 17/8), 19-shot map (xG, xGOT, situation, minute), table, head-to-head | scrape_4f0775d9a314.json (ESPN match, https://www.espn.co.uk/football/match/_/gameId/401879239/chelsea-sunderland) |
| Shots 9/10, on goal 2/4, blocked 1/1, inside/outside box 7-2 v 7-3, big chances created 2/2 and missed 3/2, touches in opposition box 14/21, passes 292/648, accurate long balls, crosses | scrape_ae904b060260.json (ESPN team stats, https://www.espn.com/soccer/team-stats/_/gameId/401879239) |
| BBC match report (penalty controversy, Palmer VAR review, "first league win since August", table 18th/5th), lineups + cards + subs with minutes, Opta-style Match Stats (possession 31.3/68.7, xG 2.5457 v 0.5306, open-play xG 1.38 v 0.32, set-play xG 0.38 v 0.21, xA, touches in box 14/21, final-third passes 35/148, crosses 9/23, tackles 23/11, fouls 17/8, yellow cards 5/4), form guide, season stats, H2H, fan-vote ratings | scrape_c74d96800865.json (BBC, https://www.bbc.com/sport/football/live/cwm23qne5pqyt) |
| Parsed shot map (team, player, minute, xG, xGOT, situation, outcome) | data/matches/chelsea-sunderland-2026-11-08/shots_espn.json |
| Derived splits (halves, penalty vs non-penalty xG, per-player shots/xG, BBC stats pairs) | data/matches/chelsea-sunderland-2026-11-08/derived.json via analysis.py |
| Search hit list (BBC, Sky, chelseafc.com pages) | search_50683cd7e56b.json, search_d1598934828e.json (snippets only) |

Notes for the analyst
- ESPN lineup shows Isidor on for Brobbey at 67'; the BBC report text says Brobbey was substituted in the 77th minute. Isidor shot at 77' as a sub, so 67' is right. Avoid quoting the minute.
- ESPN commentary says Chelsea "slip to fifth"; BBC says "stayed fifth" and the table shows Chelsea 5th on 16 points before and after. Use "fifth" only.
- Shot map outcome labels sit before each "n of 19" header in the raw page; shots_espn.json maps them correctly (Le Fée = Goal).
- Colwill played 45 minutes (replaced by Estêvão at half-time; ESPN 45', BBC 46'). Borderline for "worst" (exactly 45 min) and the penalty call he gave away was disputed, so he is not used.
- Data gap: no player ratings, no PitchAPI; Reddit only via RSS (no counts).
