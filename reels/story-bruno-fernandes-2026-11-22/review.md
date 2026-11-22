FIX (round 2)

Reviewer verdict for reel `story-bruno-fernandes-2026-11-22` (Scout Files #6), 2026-11-22. I checked the new out/reel.mp4 (rendered 18:30), timing.json and voice.wav.

All round-1 content fixes are in the audio. The on-screen subtitles were not updated: they are drawn from each beat's `caption` field, which still holds the round-1 text, so the subtitles no longer match what is spoken.

1. **Beat 0 (hook, and the cover frame):** the `caption` still reads "United's Bruno Fernandes. Player of the year. Then benched." Frame 0 and the first second show "UNITED'S BRUNO FERNANDES. PLAYER" while the frog says "Player of the year". Set the `caption` to "Player of the year. Then benched." The kicker already names the player.
2. **Beat 3:** the `caption` still has "Comment below.", and the subtitle shows "COMMENT" after that line was cut from the voice. Set the `caption` to "Was Carrick right to bench his captain?"
3. **Beat 2:** the `caption` says "Fernandes never came on." but the voice says "Bruno never came on." Make the caption say "Bruno".
4. **Beat 5:** the `caption` says "Bruno's still captain, and contract talks can wait: \"If I wanted…" and the subtitle shows "WAIT: \"IF I WANTED", but the voice says "Bruno's still captain. Contract talks? If I wanted more money, I wouldn't be here." Set the `caption` to: "12 November, Carrick was sacked. Bruno's still captain. Contract talks? \"If I wanted more money, I wouldn't be here.\""
5. **Beat 4 (optional, for consistency):** the voice now gives the full quote. The caption can stay with the ellipsis, which is accurate, or give the full verbatim line: "Everyone thought that was a punishment for the words that I had. If it was, it was right."
6. **Loudness:** the integrated level is -15.2 LUFS, against a target of about -14. Re-normalise to -14 ±1 in the same re-render.

This is a caption-only re-render: the audio and timing do not change. After it, a frame check is enough to PASS.

Checked and OK in round 2
- Hook: "Player of the year. Then benched." In voice.wav "benched" ends at about 2.43 s, inside the 3 s limit. Beat 0 ends at 2.48 s, the hook is 7 words (max 10), and the first frame shows the hook card.
- Beat 4 quote: the spoken words are verbatim from ESPN (scrape_a7b755baff64): "Everyone thought that was a punishment for the words that I had. If it was, it was right."
- Beat 1: "It's a decision from the staff to not press man-to-man" is verbatim in Sky (scrape_78c6cd1fa0ee); BBC has "man to man".
- Beat 5: "If I wanted more money, I wouldn't be here." is verbatim in BBC (scrape_09da77b3eee4, "He told Sky Sports"). Sky's video is dated 21 Nov.
- Facts are unchanged from round 1 and were re-confirmed then: Como 4-1, the benching four days later, Bournemouth 3-0 as an unused sub, "pure football", PFA + FWA Player of the Year (manutd.com), Roma 3-2 from 2-0 down, Carrick sacked 12 Nov (Guardian, BBC), still captain (manutd.com).
- caption.txt and story.json outro_question now read "after his comments".
- No `rejected` claims and no `never` items: no private life, health, legal matters, rumour or cruelty.
- Host is frog3d. The outro card asks "RIGHT TO BENCH HIS CAPTAIN?".
- Specs: 1080x1920 H.264 + AAC at 30 fps, 40.0 s (inside the 30-40 s target), 7 beats.
- Frames: no clipped or overlapping card text. The beat 3 card is fully visible from 18.7 s; at 18 s it is still animating in.
