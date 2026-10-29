FIX

1. Beat 4 (59' double change, card + say) and caption.txt: the causal claim is not supported. In the same window Chelsea's non-penalty xG also rose, 0.24 (5 shots) to 0.79 (5 shots), per derived.json. Other changes fell inside "after 59'": Colwill came on for Lacroix at 46', Chelsea made a triple sub at 68', Liverpool subbed Jacquet at 72', Mac Allister at 81' and Isak at 82' (BBC lineups). Liverpool also did not score from open play afterwards, so "The turning point" overstates it. Reword the say to something like "After Iraola's double change at fifty-nine minutes, Liverpool's expected goals, without penalties, went from zero point two five to one point oh eight." Drop "turning point". In caption.txt change "lifted" to "came before"/"went from". Optionally add "Chelsea's rose too" to the card sub. The 0.25/1.08, 5/4 and 0.05/0.27 numbers themselves check out against the ESPN shot map and BBC lineup (Wirtz and Barcola on at 59').
2. Beat 7 (say "Liverpool meet Bournemouth next", card "8 LAST"): BBC only says the draw gives Liverpool an Anfield quarter-final against Bournemouth, so "next" can read as the next fixture. Change the say to "Liverpool drew Bournemouth in the quarter-final." (or "Liverpool face Bournemouth in the last eight"). The card is fine.
3. Beat 2 banter (stamp "NO OPEN PLAY", say "Chelsea had eleven shots... only goal was a penalty"): every number is true (ESPN 11 shots, 4 on target, Rogers 40' pen), but Liverpool's only goal was also a penalty (10 shots, 4 on target), so the one-sided framing is a bit misleading. Add a clause such as "Liverpool's was too, but they won the shootout", or change the sub to "both goals pens", so the banter stays number-based and fair.

Advisory, no change needed:
- The reviewer spec says 25-60 s but the reel is 61.7 s. It is within the skill's 25-65 s limit as you said. Trim about 2 s if you want to meet the spec's cap.
- Beat 6 (Fofana as worst) is a judgement call, and the reel already says "it's close" and names Gravenberch.

Checks passed
- Facts (ESPN scrapes 7e77eb47fd74 and 36b60ed9f93d, BBC c69wz7x4jq71t):
  - Score 1-1 and pens 6-5. Goals were Rogers 40' pen and Gakpo 43' pen.
  - 18 penalties = 2 in game + 16 shootout (8 each).
  - Shootout: Liverpool 6/8 (Tsimikas missed, Gravenberch saved). Chelsea 5/8 (Barco missed, Emegha saved, Fofana off target).
  - xG 2.10 v 1.82, possession 52/48, shots on goal 4/4, saves 3/3.
  - Shots 10 v 11 (BBC match stats, ESPN percentages, shot map).
  - Mamardashvili: 3 saves from 4 on target, saved Emegha, 90 minutes.
  - Fofana: handball 43' (BBC "just three minutes later"), skied the last kick, 90 minutes. The 0.79 xG is the Gakpo pen.
  - Gravenberch conceded the 40' pen and his kick was saved.
  - Iraola is Liverpool's manager.
  - Round: Carabao Cup fourth round. Chelsea are out.
  - Names are spelled as in the data.
- Hook: the first frame is not blank. "18 PENALTIES. ZERO OPEN-PLAY GOALS." is fully visible at 0 s, and the hook is concrete and surprising.
- Frames (fps=1 8x8 tile of the whole film, plus fps=0.5 4x4): no clipped text at rest and no empty cards. The banter stamp slams in off the right edge for about 1 frame, then settles clear of the sub-line and the mascot. Mamardashvili, Fofana and outro cards are readable.
- Emotion fits: shocked on the hook, laughing on banter, smug on the shootout, excited for the best pick, disappointed for the worst pick.
- Tone: aimed at performance and numbers. No red lines in config/teams.json are crossed (no tragedy references, no personal abuse, no injury jokes). Banter is correctly on, since Chelsea lost and both clubs are rivals.
- Specs: 1080x1920, 30 fps, H.264 + AAC 44.1 kHz stereo, 61.7 s, -14.9 LUFS integrated, true peak -1.2 dBFS.
- Caption: exists. Aside from items 1 and 3, the numbers match.
