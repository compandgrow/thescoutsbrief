PASS (round 2)

The four round-1 fixes are in and each matches the cached pages:
1. Beat 3 (stat) + caption.txt now say "Liverpool signed him in a club-record £116m deal". This matches BBC (scrape_9d7b1cbfe3cd: "club record £116m", "£100m guaranteed + £16m add-ons") and Guardian (scrape_025349f74c43). The card sub still gives the £100m + £16m split.
2. Beat 2 (quote) is now reported speech ("Klopp says that over the summer, it felt like... just to look at this team") and is faithful to ESPN (scrape_a8fcc558c393). "Love at first sight" is verbatim. The quote card is unchanged and verbatim with ellipses.
3. Beat 5 (outro) now says "Klopp says no-one will question them for at least three or four months", which matches the Guardian wording (scrape_1dcfdaa97df3), "at least" included.
4. Beat 1 + caption.txt now say "This summer" instead of "Five months ago". That matches the BBC/ESPN last-32 exit to Paraguay and the card's "SUMMER 2026".
The edits add no new wording problems and nothing from `never` or `rejected`. The host is still frog3d.

Hook: beat 0 is unchanged. "Five-nil" ends at ~0.74 s (voice.wav silencedetect), so the payoff is spoken well within 3 s. The first frame shows "KLOPP'S GERMANY: 5-0."
Sheets (review_a.jpg, review_b.jpg, new MP4): cards and subtitles stay in sync, with no clipped text and no empty cards.
Specs: 1080x1920 30 fps, H.264 + AAC, 6 beats, -14.5 LUFS. Duration is 42.17 s, under the 45 s max.

Notes (not failing):
- At 42.17 s the reel is over the 30-40 s target. The question now lands at ~25 s rather than ~22 s.
- In caption.txt, "signed him" comes after lines about the team, so "Wirtz" would read more clearly there.
- Still cosmetic: a pinned note partly covers the "?" on the outro card, and the quote card has an orphan "WAS" line.
