import json,os,re
D=os.path.dirname(os.path.abspath(__file__))
sh=json.load(open(D+'/shots_espn.json'))['shots']
def m(s):
    x=re.match(r"(\d+)'(?:\+(\d+)')?",s['minute']);return int(x.group(1))+(int(x.group(2) or 0)/100)
def agg(f,team):
    r=[s for s in sh if s['team']==team and f(s)]
    return dict(shots=len(r),goals=sum(s['outcome']=='Goal' for s in r),xg=round(sum(s['xg'] for s in r),2),sot=sum(s['outcome'] in('Goal','Saved') for s in r))
out={}
for t in('MAN','AVL'):
    out[t]={'all':agg(lambda s:True,t),'first4min':agg(lambda s:m(s)<=4.0,t),
     'pre_45':agg(lambda s:m(s)<45.01 and "'+" not in s['minute'][:0] ,t),
     'h1':agg(lambda s:m(s)<46 and not (s['minute'].startswith('45') and False),t),
     'h2':agg(lambda s:m(s)>=46 and True,t),
     'min5_to_43':agg(lambda s:4<m(s)<44,t),
     'nonpen':agg(lambda s:s['situation']!='Penalty',t),
     'after_89':agg(lambda s:m(s)>=89,t),
     'after_4_2':agg(lambda s:m(s)>=53.0 ,t)}
print(json.dumps(out,indent=1))
