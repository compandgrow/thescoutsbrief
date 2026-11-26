FIX

# Review: manchester-united-sporting-cp-2026-11-25 (round 1)

Verdict: FIX. One fix only. Every fact checks out, and the frames, tone and specs are clean. The hook breaks the format v4 hook rule.

1. **Beat 0 (hook), `say`**: the payoff arrives after 3 s and has build-up in front of it. "Two-two in Lisbon." runs from 0.05 to 1.37 s (silence 1.37 to 1.73 s in audio/voice.wav). The payoff sentence then runs from 1.73 to 4.27 s, so "United's keeper" lands at about 3.4 to 4.2 s. That misses `hook.payoff_within_s` = 3, and it breaks the rule "No build-up before the payoff." The 2-2 scoreline is already on the kicker and the pill.
   Change `say` to: "Both Sporting goals started with United's keeper." (7 words). Keep the card, the emotion and the hit as they are. Then re-voice and re-render, and confirm in timing.json that beat 0 ends at or before about 3.0 s.

## Verified OK
- **Facts (cached pages opened):**
  - xG 2.46 / 1.07: ESPN match page scrape_ca3883766b8d ("Expected Goals" 2.46) and ESPN commentary scrape_7fbbb38fc679 ("1.07 to their opponents' 2.46").
  - 33' penalty 0.79 and 80' goal 0.46: shots_espn.json n=5 and n=16, with 0.79 and 0.46 present in scrape_ca3883766b8d. The sum is 1.25, which matches derived.json SCP_xg_from_lammens_errors. It is labelled "Scout calc", as the caveats require.
  - Penalty save, then gave away the second: ESPN report scrape_840f5f5b714c ("saved a Luis Suárez penalty only to gift Sporting another").
  - Dropped cross at 80' with United 2-1 up: ESPN commentary 80' "fails to gather Fresneda's high cross" and Guardian scrape_a11766a86fa1 "Cruising, it seemed, at 2-1 and with 10 minutes left ... Lammens dropped a high ball". The wording "dropped a cross" follows the caveat.
  - Two United goals ruled out by the referee: BBC scrape_fa0b680d039a ("VAR could not intervene as Marciniak had blown his whistle"; "reversed his decision after spotting an infringement by Patrick Dorgu") and the ESPN report ("a pair of controversially ruled out goals").
  - Pochettino's first win: ESPN report ("denied Mauricio Pochettino a first win in charge"; "began with a chastening 4-0 loss at rivals Liverpool"), Guardian ("heading for a first victory under Pochettino") and manutd.com scrape_3620b2bb15e3 (4-0 at Anfield, first game). This is trends t1, strength strong. Caption "2 games, 0 wins" matches t1.
  - BBC users 2.91: BBC page "S. Lammens Average Rating: 2.91", the lowest of all 31 ratings (next lowest 3.92). BBC mark 3: "How they rated" "Senne Lammens: Shocking mistake ... **3**".
  - +0.69 goals prevented: ESPN player stats scrape_6f0cf5a4cb9b, Lammens row GP 0.69.
  - The name Senne Lammens is spelled as in the data.
- **Frames** (review_a.jpg, review_b.jpg, frame 0, full-res frame at 25 s):
  - Frame 0 is the hook card ("BOTH SPORTING GOALS: UNITED'S KEEPER") and is not blank.
  - No clipped, overlapping or empty cards. Captions match each card's topic.
  - Emotions fit their beats: shocked, disappointed, neutral then smug, disappointed then angry, happy. The angry emote lands on "errors weren't".
  - The player card reads "+0.69" correctly.
- **Tone and banter:**
  - Anger is aimed at the errors and backed by numbers. There are no personal insults.
  - Result banter is false (draw; Sporting are not a watched club), and there is no banter beat. No red line in config/teams.json is crossed.
- **Trends:**
  - trends.json exists, and fan_buzz.status records the Reddit attempt (404).
  - No fan-opinion claims are made. The question frames the outlets' angle, as in reel_angle.
  - The only trend claim used is t1 (strong). Nothing from `rejected` appears (no form run, red-card count or Villa howlers).
- **Specs:**
  - 1080x1920, H.264 + AAC, 32.77 s (target 28-35, max 40), 5 beats.
  - 74 spoken words (max 110). Longest beat is 7.88 s (max 8).
  - -14.9 LUFS integrated.
- **Caption:**
  - caption.txt exists. The first line holds the hook and the debate question.
  - It has 9 hashtags, and every claim is sourced as above.

## Notes (not blocking)
- On the compare card, "GOALS IT COST UNITED: 2 ruled out" counts the second (VAR) decision against the referee. ESPN calls both decisions controversial and the BBC pundit line says the goal "should have stood". It is framed as a debate question, so it can stay.
- BBC user ratings may still move slightly. They are credited "BBC USERS" on screen.
