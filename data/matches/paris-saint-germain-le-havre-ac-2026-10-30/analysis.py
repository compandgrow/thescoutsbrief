"""Le Havre 1-5 PSG (30 Oct 2026). Goal timeline from the PSG.fr report; checks the numbers in insights.json. Rerun: python3 analysis.py"""
goals = [(18, "HAC", "Maja"), (26, "PSG", "Godts"), (28, "PSG", "Hakimi"), (55, "PSG", "Hakimi"), (62, "PSG", "Mayulu"), (69, "PSG", "Hakimi")]
assert sum(t == "HAC" for _, t, _ in goals) == 1 and sum(t == "PSG" for _, t, _ in goals) == 5
print("Hakimi goals:", sum(p == "Hakimi" for _, _, p in goals))
print("PSG after going 1-0 down:", sum(t == "PSG" for m, t, _ in goals if m > 18))
print("Pass accuracy HAC %.0f%% PSG %.0f%%" % (243 / 303 * 100, 711 / 777 * 100))
