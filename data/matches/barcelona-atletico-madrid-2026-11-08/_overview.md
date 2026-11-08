# Atlético Madrid 1-2 Barcelona (ESPN 401882816) - 2026-11-08, Spanish LaLiga (web path, no PitchAPI)

Home: Atlético Madrid (ATM), away: Barcelona (BAR). Final 1-2 (ESPN/BBC list Atlético first). Winner BAR, loser ATM. Goals: G. Simeone 10' (ATM); Fermín López 45', 66' (BAR). Both clubs are watched rivals (not favourites); ATM lost, so banter applies. No player ratings exist: label best/worst as "Scout's pick".

Raw files (all under /home/user/thescoutsbrief/data/):
- matches/barcelona-atletico-madrid-2026-11-08/shots_espn.json - 28 shots with minute, outcome, xG, xGOT, situation (9 ATM, 19 BAR; matches team shot totals). Minutes like "45'+3'" are first-half stoppage time.
- matches/barcelona-atletico-madrid-2026-11-08/_web_sources.json - source URLs.
- research/scrape_c8eaa32ec14b.json - ESPN UK match page (https://www.espn.co.uk/football/match/_/gameId/401882816/barcelona-atletico-madrid): score, scorers, formations (ATM 4-4-2, BAR 4-1-4-1), substitutions with minutes (de Jong on at 45' here), Match Leaders (Álvarez 4 shots, 1 SOG, 0.24 xG; F. López 6 shots, 3 SOG, 0.92 xG; saves; passes), standings 11-0-1 33 pts (BAR), 9-1-2 28 pts (ATM).
- research/scrape_f99b15b08015.json - ESPN team stats (https://www.espn.com/soccer/team-stats/_/gameId/401882816): shots 9/19, SOG 4/4, blocked 1/5, attempts inside/outside box, big chances created 3/1, big chances missed 3/2, touches in opposition box 19/27, corners 4/2, passes 391/675, accurate passes 81%/91%. No possession figure.
- research/scrape_d0a74296d387.json - BBC match page (https://www.bbc.com/sport/football/live/cm4g1jlw7vqlt): match report text, live posts, Basic and In-depth Match Stats (possession 37/63, shots, tackles 30/15, tackle win % 53.3/86.7, yellow cards 4/1, offsides 5/1, final-third passes 56/141), La Liga table (BAR 1st 33 pts, ATM 3rd 28 pts, last-6 league form), line-ups with managers (Simeone, Flick), formations (4-4-2, 4-1-4-1), cards and subs (de Jong on at 46' here), season-so-far stats, form guide.
- research/search_cf6cc459b22c.json, research/search_7c8cbadf33b5.json - searches (ESPN live blog preview, fcbarcelona.com previews).
- form/83.json (BAR, includes this match) and form/1068.json (ATM, ends 2026-11-03, does NOT include this match).

Notes for the analyst:
- No ratings: best/worst = Scout's pick, built from shots/xG/goals; say so in caveats.
- ESPN and BBC disagree on the de Jong substitution minute (45' vs 46'): say "at half-time", no exact minute.
- ESPN Match Leaders xG (López 0.92, Álvarez 0.24) differ by 0.01 from summing the shot map (0.93, 0.23): use ESPN's player figures; team xG totals are sums of the shot map.
- ESPN shows Oblak facing 5 SOGA while both sources give Barcelona 4 shots on target: avoid goalkeeper save-ratio claims.
- BBC live blog mentions a pre-match tribute: do not use it (red lines).
- Skip off-pitch material (tifo about Álvarez's summer).
