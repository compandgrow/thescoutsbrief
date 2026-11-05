# as-roma-manchester-united-2026-11-03 — 24 h review (45.9 h data age after posting; day-1 row from timeline)
Scores: hook 57.7% skipped · held 7.26s of 31.4s (0.234) · 0.0/1k reach shares+saves · 0 comments · 185 views
vs channel median (12 reels, match series): hook better (57.7% vs 58.4%, within noise), held better (0.234 vs 0.173), value same (0.0 vs 0.0). Fixed bars: hook under the 60% fail line, held just under the 0.25 bar (second best on the channel behind arsenal-liverpool 0.274), value zero. 1 like, 0 comments, 0 shares, 0 saves, 0 profile views, 0 replays. Day-1 row (4 Nov): 184 views, 166 reach, 1 like, follows 0 (single-post call returned follows null). Data barely moved from day 1 to day 2.
Main reason: the hook states the matched pair ("Seven Roma shots before half-time. Zero after.") but about the team that lost, so the viewer learns the twist happened but not what it meant; the payoff the audience cares about (United ending nine games without a win, Cunha's two goals in three minutes) sat at beat 2 (11.3 s) and beat 3 (16.2 s), after the average viewer (7.26 s) left.
Viewers left during: beat 1 "United flipped it. Five shots before the break, ten after. All three goals came in the second half." (4.12–11.01 s). The average viewer left about 45% of the way into it, on "ten after".
What worked:
- Hold: avg watch 7.26 s, the second longest on the channel, with a 31 s cut (ratio 0.234 vs 0.173). The hook was short (3.3 s, 8 words) and the first beat started at 4.1 s.
- Hook skip 57.7% vs 58.4% median: the matched-numbers shape ("7 before, 0 after") does not skip worse than average but does not beat the pure contrasts ("Seventeen shots. Zero on target.", 54.7%; "Nineteen shots to nine.", 49.6%).
- The talking-point angle (t1, nine games without a win) is the strongest story in the set, and it is the one trend with "use_for: hook".
What should have worked:
- Put the trend in the hook, as trends.json suggests (`hook_angle`: "Nine games without a win. Then Roma had zero second-half shots."). Spoken: "Nine games without a win. Then Roma had zero second-half shots." (11 words) with card "9 GAMES.\nNO WIN.\n*0* ROMA SHOTS AFTER HALF-TIME." Keeping the pair gives the viewer both the stake and the twist in the first 4 s, and the favourite-club angle (United) is in the first line.
- Beat 1 as a 2-row compare read in 7 s was where people left; the same numbers are already on the hook card. Replace it with the story: "Two-nil down at home after 17 minutes. Then Cunha: two goals in three minutes." (all in insights.json: Cunha 83', 86').
- A 24-25 s cut that ends with the Carrick question; the "retaken penalty" caveat at 27 s is good journalism and should be kept, but nobody reached it.
Test next time: when a trend with `use_for: hook` exists, open on the trend number (streak, drought, milestone) and put the match twist second in the same sentence; don't open on the opponent's numbers.

Notes: angle_source talking_point, no banter (favourite won; the banter option was the nine-game drought itself). Posted 25 h after full time at 01:29 UTC Wednesday.
