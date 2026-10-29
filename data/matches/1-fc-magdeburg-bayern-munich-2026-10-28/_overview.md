# Bayern Munich 6-1 1. FC Magdeburg - German Cup (DFB-Pokal), Round 2, 28 Oct 2026
espn_id 401917035. Web path (no PitchAPI). No player ratings: best/worst = "Scout's pick". No shot map (shots_espn.json is empty): use goals/timeline.
Favourite (Bayern) played and won: no banter, not a rival loss.

## Cached files (data/research/)
- scrape_085802ec5045.json / scrape_d529cf143364.json (both ESPN UK match page https://www.espn.co.uk/football/match/_/gameId/401917035/1-fc-magdeburg-bayern-munich): data.markdown has the header scorers+minutes (Olise 10', 50' pen; Saibari 21'; Davies 70'; Brown 73'; Daiber 90'+3'; Zukowski 15' for Magdeburg), PA report blurb (Kane rested on bench), "Team Stats" (possession 63/37, shots on goal 8 v 2, passes 745 v 430, saves 1 v 2, tackles, clearances).
- scrape_afb8be22c773.json (BBC https://www.bbc.com/sport/football/live/cqe9l1yej078t; ignore the junk 'edigitalsurvey blocked' header): formations (4-2-3-1 v 4-3-3), lineups with sub minutes and cards, Match Stats/Opta (shots 19 v 9, on target 8 v 2, touches in opp box 64 v 11, final-third passes 317 v 23, possession 63.3/36.7, crosses 10 v 2, woodwork 0 v 1, long balls 42 v 61, clearances 7 v 23), Live Text (only last events, page 1: Daiber goal assisted by Stanisic after fast break).
- shots_espn.json: empty. _web_sources.json: source URLs.

## Caveats for the analyst
- Kane: in BBC substitutes list, never appears as a substitution -> did not play. ESPN/PA: "left on the bench".
- Assist/goal-type detail exists only for the 90+3' goal (BBC live text).
- ESPN logo alt text mislabels Bayern as "MUN": ignore.
