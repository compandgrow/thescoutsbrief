PASS

Reel: celta-vigo-real-madrid-2026-11-21 (Real Madrid 2-1 Celta Vigo, LaLiga, favourite win, no banter). Reviewer round 1.

## Facts (each opened in the cached raw file)
- Hook 24 v 8 shots: ESPN team stats (data/research/scrape_9644e9ecf75e.json, "24Shots8"); shots_espn.json has 24 RMA / 8 CEL shots.
- Big chances missed 5 v 0: same file, "5Big Chances Missed0". xG 3.75 v 1.64: ESPN match page Team Stats (scrape_0f6773c67f43.json).
- "Mbappé skied a penalty": ESPN report (scrape_2b49b105c142.json) "sent his penalty sailing over the crossbar"; shot map shot 15, 39', Penalty, Off Target. Reuters agrees.
- 57' triple sub, before 15 shots / 0 goals, after 9 shots / 2 goals: recomputed from shots_espn.json by analysis.py (derived.json RMA_before_57 / RMA_after_57). Three subs at 57' (Cucurella, Valverde, Vinícius) are in the ESPN lineups. The reel does not say who Vinícius replaced (sources disagree).
- Vinícius 0.71 xA, 2 big chances created, on at 57': ESPN player stats (scrape_20b27ea37a9c.json, row "| 26 | 0 | 0 | 0.01 | 0.71 | 0 | 1 | 2 |"). It is labelled "Scout's pick" (no ratings on the web path). The reel does not claim assists (ESPN gives him 0).
- Espí: 5 touches, 1 goal, on at 79', 85' winner, header saved then rebound scored: ESPN player stats ("| 5 | 1 | 0 | 0.93 |"), commentary 79' sub and 85' save/goal, ESPN report.
- "Level with Barça, for now": trends.json t1 (strong). Reuters "level with leaders Barcelona, but have now played a game more", plus the ESPN report/table and the BBC table. "For now" covers Barcelona's game in hand.
- Names are spelled as in the ESPN data (Vinícius Júnior, Carlos Espí, Mbappé).

## Watch (review_a.jpg, review_b.jpg, frame0.jpg)
- Frame 0 is the cover: "REAL MADRID 2–1 CELTA / SHOTS / MADRID 24 / CELTA 8" in full, with the LaLiga blue theme.
- No text is clipped or overlapping, and no card is empty. Captions match the card topic on every beat. The player card shows 3 tiles with no rating badge.
- Emotions: shocked (hook), disappointed (waste/penalty), excited (sub), happy (pick), excited→smug (Espí), happy (outro). There is no anger, and Mbappé's miss is stated plainly.

## Hook
- 10 words. "Twenty-four shots" is spoken at about 1 s and "Celta, eight" at about 2.5-3.0 s (caption frames at 2.5/3.0 s), so the payoff lands within 3 s. Both clubs are named with the same measure (format.json/learnings rule).

## Tone / banter
- banter false (a favourite won), so there is no banter beat, which is correct. No red lines are crossed. The report's pre-match tribute to a deceased player is not referenced anywhere.

## Trend step
- trends.json exists. The Reddit step was attempted and logged (RSS 404 on the match search and on r/realmadrid). The reel makes no fan-opinion claims. t2 (form run) is not used and nothing from `rejected` is used.

## Specs
- 1080x1920, H.264 + AAC, 30 fps, 34.53 s (target 28-35, max 40), 6 beats (beats 5.4 / 5.5 / 5.8 / 5.8 / 4.3 / 4.8 s, all 8 s or less), 66 spoken words, integrated loudness -14.8 LUFS. Voice: IndexTTS 2.5.

## Caption
- First line: the hook (both clubs, same measure) plus the debate question. 10 hashtags. Every number has a source (ESPN, ESPN shot map, ESPN player stats, Reuters/BBC table).

## Notes (not blocking)
- The question still comes at about 29 s, not at the ~11 s the learnings experiment asks for. The two names are set up with a stat each in beats 3-4 (17-28 s).
