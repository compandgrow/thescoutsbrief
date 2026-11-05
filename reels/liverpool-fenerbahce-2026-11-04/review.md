FIX (round 1)

1. Beat 4 (player card, say): "and the goal that turned it" is not supported. Greenwood's free kick (29', xG 0.03) made it 1-1; Liverpool then led 2-1 at 69' (Isak). The goals that turned the match were Brown 73' and Muriqi 79'. Change the line to something the data backs, e.g. "Best on the pitch, my pick: Greenwood. A deflected free-kick goal and four shots." (BBC text: free-kick deflected off Jacquet). Re-render voice, timing and captions for that beat.
2. caption.txt: config/format.json requires the debate question in the FIRST line (debate_question_in_caption_first_line). Move it up, e.g. first line "Set pieces or finishing? Liverpool: 22 shots, 12 corners, lost." (keep it 8 words or fewer if the hook rule applies to the question line, otherwise put the question first and the hook second).

Notes (non-blocking):
- Beat 3 speaks about the two goals in six minutes and corner/throw-in (source ESPN shots_espn.json #31,32), but the card source says only "BBC Sport match stats". Add "ESPN shot map" to that source.
- Hook: 9 words, "twenty-two shots" lands inside 3 s, "lost" ends about 4.6 s (timing.json is beat-level only, so I could not check word times). First frame shows 22 / 12 / LOST. Acceptable.
- data/matches/.../_web_sources.json lists bbc_match as c6rmy8zvwnryt, which is the AEK v Real Madrid page. The reel and insights correctly use cmpdgp57zz94t. Fix the manifest.

Verified OK: 22 shots, 12 v 4 corners, 67.6% possession, crosses 42 v 10, Fenerbahce 19th (5 pts) pre-match, all in scrape_727a33bd13e7.json (BBC cmpdgp57zz94t). Greenwood 4 shots and 1 goal match shots_espn.json (#10, 14, 17, 29). 69' Isak, 73' Brown (corner), 79' Muriqi (throw-in) match. Spelling matches the data. Banter: Liverpool is a rival, no favourite lost, and every joke is a number. No red lines crossed. The tone is clean. The laughing presenter is in beat 1. No fan or trend claims. Specs: 1080x1920, H.264+AAC, 31.5 s, 5 beats, -14.9 LUFS. Frames: no clipped text, first frame is the hook.
