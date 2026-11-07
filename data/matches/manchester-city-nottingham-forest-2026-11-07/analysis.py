import json,re,os
d=os.path.dirname(os.path.abspath(__file__))
sh=json.load(open(d+'/shots_espn.json'))['shots']
def half(m): return 1 if int(re.match(r"\d+",m).group())<=45 and "+" not in m.replace("45'+","X") or m.startswith("45'+") else 2
out={}
for t in('NFO','MNC'):
    for h in(1,2):
        s=[x for x in sh if x['team']==t and half(x['minute'])==h]
        out[f'{t}_H{h}']={'shots':len(s),'xg':round(sum(x['xg'] for x in s),2),'goals':sum(x['outcome']=='Goal' for x in s),'xgot':round(sum(x['xgot'] for x in s),2)}
    s=[x for x in sh if x['team']==t]
    out[t]={'shots':len(s),'xg':round(sum(x['xg'] for x in s),2),'goals':sum(x['outcome']=='Goal' for x in s)}
print(json.dumps(out,indent=1))
for p in('L. Delap','J. Cunha'):
    s=[x for x in sh if x['player']==p]; print(p,len(s),round(sum(x['xg'] for x in s),2),round(sum(x['xgot'] for x in s if x['outcome']=='Goal'),2),sum(x['outcome']=='Goal' for x in s))
g=[x for x in sh if x['outcome']=='Goal' and x['team']=='NFO']; print('NFO goals xG',round(sum(x['xg'] for x in g),2))
