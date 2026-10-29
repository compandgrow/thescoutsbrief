"""Bayern 6-1 Magdeburg (28 Oct 2026). Scout's-pick scores from cached pages. Rerun: python3 analysis.py"""
import json
# Goals (ESPN match page header) as (player, team, minute); 90+3 -> 93
goals = [("Olise","BAY",10),("Zukowski","FCM",15),("Saibari","BAY",21),("Olise","BAY",50),("Davies","BAY",70),("Brown","BAY",73),("Daiber","BAY",93)]
pens = {("Olise",50)}
# Minutes on pitch (BBC lineups): starters subbed off at X, subs on at Y
minutes = {"Olise":68,"Saibari":75,"Davies":44,"Brown":90,"Daiber":8,"Zukowski":90,"Reimann":90}
# Best: 3 pts/goal (2 for a penalty goal's creation is not discounted: keep simple), +0.5 per extra goal beyond 1 is not needed.
best = {}
for p,t,m in goals:
    if t=="BAY": best[p] = best.get(p,0)+3
best_ranked = sorted(best.items(), key=lambda kv:(-kv[1], -minutes[kv[0]]))
# Worst (45+ min only): goalkeeper-agnostic rule = goals conceded per shot on target faced, plus team box exposure
sot_faced, conceded = 8, 6          # ESPN Shots on Goal 8 v 2; Bayern goals 6
saves = sot_faced - conceded        # = 2 (ESPN Team Stats saves FCM 2)
out = {"best_score_points": best_ranked, "reimann": {"minutes":90,"sot_faced":sot_faced,"conceded":conceded,"saves":saves,"save_pct":round(saves/sot_faced*100)},
       "halves": {"BAY":[2,4],"FCM":[1,0]}, "halftime": "2-1"}
print(json.dumps(out, indent=1))
