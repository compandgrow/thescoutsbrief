# Nice 2-3 Paris Saint-Germain, French Ligue 1, 2026-11-21, Allianz Riviera (Nice)
Goals (ESPN): Mohamed Amoura 8' (NICE); Senny Mayulu 31' pen (PSG); Désiré Doué 32' (PSG); Ferran Torres 85' (PSG, assist Ousmane Dembélé per ESPN commentary); Ali Abdi 90'+5' (NICE, assist Jonathan Clauss).
Favourite (PSG) played and won away: banter false, banter_by_favourite false, favourite_lost false (data/queue.json).
Web path (no PITCHAPI_API_KEY). NO player ratings on this path: label best/worst as "Scout's pick".
Managers (BBC lineups): Nice Olivier Pantaloni, PSG Luis Enrique. Referee Jerome Brisard, VAR Clément Turpin (BBC Match Officials).
Formations (ESPN + BBC): Nice 3-4-2-1, PSG 4-3-3. No shape change stated in any source.
Nice XI (BBC): Diouf; Mandza, Ndayishimiye, Seidu; Nkounkou, Boudaoui, Witsel (c), Clauss; Amoura, Diop; Wahi.
Nice subs (BBC/ESPN): Sanson for Diop 62'; Abdi for Mandza 66'; Hein for Amoura 67'; Coulibaly for Witsel 78'; Ngoumou for Wahi 78'.
PSG XI (BBC): Safonov; Hakimi (c), Zabarnyi, L. Hernández, Nuno Mendes; Zaïre-Emery, João Neves, Fabián Ruiz; Akliouche, Mayulu, Doué.
PSG subs (BBC/ESPN): Ferran Torres for Doué 44' (INJURY: ESPN report, Doué stretchered off, right knee, 39'; "serious" per ESPN headline — red line, never mock, keep any mention sympathetic/neutral); Dembélé for Mayulu 61'; Pacho for Nuno Mendes 61'; Godts for Akliouche 62'; Marquinhos for L. Hernández 79'.
Cards (BBC): Boudaoui 54', Seidu 75' (NICE). PSG none.

## Cached files (data/research/) and what is in them
- scrape_e2d75ed17d06.json = ESPN match page https://www.espn.co.uk/football/match/_/gameId/401876398/paris-saint-germain-nice (fetched 2026-11-21T23:49:10Z): score, scorers with minutes, records after match (NICE 5-2-4 17 pts, PSG 8-2-1 26 pts), formations/lineups/subs, Match Leaders (Abdi 2 shots 1 SOG 0.43 xG; Hakimi 2 shots 1 SOG 0.13 xG; Seidu 46 acc passes, 10 def. interventions; J. Neves 130 acc passes of 141, 7 def. interventions; Diouf 2 saves, 5 SOGA, 1.90 xGC; Safonov 1 save, 3 SOGA, 0.78 xGC), 18-shot map (Team Stats section: xG 0.78 v 1.90, possession 37% v 63%, shots on goal 3 (75%) v 5 (36%), big chances created 2 v 2, corners 1 v 5, accurate passes 353 (81%) v 705 (92%), duels won 43 v 32, saves 2 v 1, fouls 11 v 12), Ligue 1 table after match (PSG 1st 26 pts, Lille 2nd 21 pts from 11 GP; Nice 7th 17), news headlines on Doué's knee injury.
- scrape_63ddce9ab04f.json = ESPN team stats https://www.espn.com/soccer/team-stats/_/gameId/401876398 (fetched 2026-11-21T23:50:10Z, Firecrawl): Shots (shots 4 v 14, on goal 3 v 5, blocked 1 v 1, woodwork 0 v 0, inside box 3 v 7, outside 1 v 7), Attack (big chances created 2 v 2, big chances missed 0 v 1, through balls 0 v 4, touches in opp box 7 v 22, fouled in final third 0 v 4, corners 1 v 5), Passes (accurate 353 (81%) v 705 (92%), passes 434 v 764, forward zone passes 154 v 485, accurate long balls 24 v 16, accurate crosses 1 v 2).
- scrape_3e1d35bcc3b7.json = BBC Sport match page https://www.bbc.com/sport/football/live/cwdd16gddm4jt (fetched 2026-11-21T23:50:22Z, Firecrawl): Ligue 1 table (BBC, "Last Updated 21st November 2026 at 18:17", before the 19:45 games: PSG 1st 26 pts, Nice 6th 17; PSG league form last 6 = W W W W W W), lineups with managers/subs/cards, officials, Opta Match Stats (possession 36.7 v 63.3, shots 4 v 14, SOT 3 v 5, off target 0 v 8, touches in opp box 7 v 22, saves 2 v 1, aerials won 6 v 5, fouls 11 v 12, corners 1 v 5, out-of-box attempts 1 v 7, one-on-one attempts 1 v 0, offsides 3 v 3, total passes 434 v 762, pass accuracy 81.3 v 92.3, successful final-third passes 40 v 194, long balls 51 v 34, crosses 11 v 11, tackles 22 v 13, won tackle % 81.8 v 61.5, yellow cards 2 v 0, clearances 14 v 13), season so far (goals 17 v 25, conceded 15 v 12, points gained from losing position 7 v 11), form guide all comps (PSG last 5 before this game: W Troyes 1-0, W Villarreal 6-0, W Le Havre 5-1, W Lyon 2-0, W Barcelona 4-2), previous meetings, live text page 1 only (≈ 79' to FT). NB no BBC xG on this page; use ESPN xG.
- scrape_99f31d0a9174.json = ESPN report https://www.espn.co.uk/football/report/_/gameId/401876398 (free local fetch): AP story on Doué (stretchered off, right knee, 39th minute, no contact; had scored his second league goal of the season; Torres replaced him; PSG face Roma in the Champions League on Wednesday; Kvaratskhelia ACL tear v Barcelona Oct 20, Dembélé and Marquinhos thigh tears in that game; Dembélé came off the bench).
- scrape_f0a570fbac50.json = ESPN commentary https://www.espn.co.uk/football/commentary/_/gameId/401876398 (free local fetch): 79' to FT only. Torres goal 85' assisted by Dembélé; Dembélé also assisted Ruiz 85' (off target), Hakimi 90'+1' (saved), Neves 90'+1' (blocked header).
- shots_espn.json (local): 18 shots (NICE 4, PSG 14), xG/xGOT/minute/situation. Matches team stats counts (4 v 14). Sums 0.78 / 1.91 (rounding); use the header 0.78 / 1.90.
- _web_sources.json (local): the three Firecrawl/ESPN/BBC URLs above.

## Gate
Score: yes. Team stats: yes (ESPN + BBC Opta). Shots: yes (18). Lineups: yes. PASS.

## Caveats for the analyst
- No player ratings. Best/worst = "Scout's pick".
- Doué injury (stretchered off, knee): red line. No mocking; the presenter's team, so sympathy only, or leave it out.
- League tables differ by update time: BBC (18:17) Nice 6th; ESPN (later, after Lille v Lyon) Nice 7th, Lille 2nd on 21. Prefer ESPN for "after tonight"; avoid Nice's position on screen.
- Commentary only covers 79'+, so Dembélé's full assist/chance count is not available; only "assisted Torres' goal" is safe, plus the 3 other attempts he set up from 79' (lower bound).
