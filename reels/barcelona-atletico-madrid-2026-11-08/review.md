# Review: barcelona-atletico-madrid-2026-11-08
Verdict: PASS (fix rounds used: 0 reviewer rounds; 1 producer layout fix before review)

Checked: shots_espn.json recount (ATM 7 shots/1.37 xG first half, 2/0.15 after, 0 on target after; last SOT Baena 38'), possession 37/63 and passes 391/675 (insights.json, BBC/ESPN), Fermin Lopez 2 goals/6 shots/0.92 xG (ESPN match leaders), back-to-back home defeats (t2 strong, form/1068.json: Bayern 0-2 H 3 Nov + this match). Fan question matches trends fan_buzz. Banter allowed (rival lost, no favourite), every joke numeric, no red lines. 1080x1920 H.264+AAC, 41.7 s, 6 beats, -14.5 LUFS. First frame shows the hook.

Flags (not failures):
- Hook: "seven shots" is spoken at ~1.5-3.5 s, but the contrast word "Two after" lands at 3.85-4.5 s, just past hook.payoff_within_s=3 (learnings allow 4 s). 7 words <= 10.
- Banter at beat 1 puts the xG card before the compare "proof" slot (structure order is tunable, not locked); it carries the numbers that back the hook, so not a hard-rule break. Compare is 2 rows (experiment).
- Banter line "Nothing on target" means second half only; the card sub says so.
- Player card trimmed to 2 stats (goals, xG); spoken line also gives six shots.
