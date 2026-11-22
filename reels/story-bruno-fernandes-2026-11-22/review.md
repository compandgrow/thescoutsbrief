FIX

Reviewer verdict for reel `story-bruno-fernandes-2026-11-22` (Scout Files #6), 2026-11-22.

1. **Beat 0 (hook): the payoff lands too late.** In voice.wav, "United's Bruno Fernandes." runs 0.05-1.85 s, "Player of the year." runs 2.15-3.15 s and "Then ... benched." runs 3.41-4.63 s, so "benched" is not heard until about 4.0-4.6 s. The rule (format.json hook.payoff_within_s = 3, plus stories.json cold_open) needs it inside 3 s. Change `say` to "Bruno Fernandes: player of the year, then benched." with no long pauses, or open on "Player of the year. Then benched." and leave the name to the kicker card. Re-time the beat so that "benched" ends before 3.0 s. The card can stay as it is.
2. **Beat 4 (twist): the spoken quote is not verbatim.** The `say` text reads "Everyone thought that was a punishment. If it was, it was right." ESPN (data/research/scrape_a7b755baff64.json) has: "Everyone thought that was a punishment for the words that I had. If it was, it was right." The voice cannot show the ellipsis, so the cut goes unmarked. Change `say` to: "The twist? Bruno agreed: everyone thought that was a punishment for the words that I had. If it was, it was right." The card and caption already mark the cut with "…" and are OK.
3. **caption.txt: the question assumes a motive that is in dispute.** "Was Carrick right to bench his captain for speaking out…" treats the benching as punishment for speaking out. Carrick called it a "pure football" decision (Sky, scrape_78c6cd1fa0ee). Fernandes says Carrick told him it had "nothing to do with the words of Como" (BBC, scrape_09da77b3eee4). Change it to: "Was Carrick right to bench his captain after his comments, or should a club's best player be allowed to say it?" The same wording is in story.json `outro_question`, so align it there if it is reused.
4. **Length (not a fail, but fix with 1-2):** the video is 43.0 s. That is under the 45 s max but over the 30-40 s target, and item 2 adds about 1.5 s. To get back to 40 s or less, drop "Comment below." from the beat 3 `say` (the card already shows COMMENT BELOW) and tighten the hook as in item 1. In beat 5, "Bruno's still captain, and contract talks can wait." can become "Still captain. Contract talks can wait."

Checked and OK
- Sources opened: Sky scrape_78c6cd1fa0ee, BBC scrape_8992742d9605, ESPN scrape_a7b755baff64, BBC scrape_09da77b3eee4, manutd.com scrape_70fd7f9cdf86, Guardian scrape_2603dba5c82d, AP scrape_9c23f8f04c40, BBC scrape_d2f8191d8fa1.
- "It's a decision from the staff to not press man-to-man" is verbatim in Sky. BBC has the same words with "man to man". The words were spoken to TNT after Como 4-1, a Champions League game.
- "Four days later … 3-0 Bournemouth … never came on": Sky ("unused substitute … did not come on"), AP ("four days after") and BBC. "Pure football" is in Sky.
- "Player of the year": manutd.com (official) says "reigning PFA and FWA Player of the Year", and ESPN says "England's Footballer of the Year last season".
- 3-2 Roma win after being 2-0 down: ESPN. The penalty claim (rejected) is not used.
- Carrick sacked 12 Nov: Guardian and BBC. Still captain: manutd.com (Pochettino).
- "If I wanted more money, I wouldn't be here." is verbatim in BBC ("He told Sky Sports"). The Sky video is dated Sat 21 Nov 2026, so the card's attribution is correct. The "not the right time" / talks-paused claim is supported by BBC and Sky.
- Nothing from `rejected` is used. Nothing about private life, health, legal matters, rumour or pundit cruelty. Neville and Carragher are not used.
- Host is presenter frog3d. The outro card asks the question "RIGHT TO BENCH HIS CAPTAIN?".
- Frames (out/review_a.jpg, out/review_b.jpg): the first frame shows the hook card "PLAYER OF THE YEAR. THEN BENCHED.". No text is clipped or overlapping and no card is empty. Captions match each card's topic.
- Specs: 1080x1920 H.264 + AAC at 30 fps, 43.0 s, 7 beats (5-8 allowed), -14.9 LUFS integrated.
