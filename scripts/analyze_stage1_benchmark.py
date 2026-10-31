from __future__ import annotations
import argparse,csv,json,re,statistics
from pathlib import Path
from collections import defaultdict,Counter

def toks(s):return set(re.findall(r'[a-zA-Z]{3,}',s.lower()))
def jac(a,b):
 A,B=toks(a),toks(b)
 return len(A&B)/len(A|B) if A and B else 0.0
def pair(vals):
 xs=[]
 for i in range(len(vals)):
  for j in range(i+1,len(vals)):xs.append(jac(vals[i],vals[j]))
 return statistics.mean(xs) if xs else 0.0
def mean(xs):return statistics.mean(xs) if xs else None

def load(paths):
 rows=[]
 for p in paths:
  for line in Path(p).read_text(encoding='utf-8').splitlines():
   if line.strip():rows.append(json.loads(line))
 return rows

def main():
 p=argparse.ArgumentParser();p.add_argument('traces',nargs='+');p.add_argument('--out',required=True);a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 rows=load(a.traces); valid=[r for r in rows if r.get('normalized')]; groups=defaultdict(list)
 for r in valid:groups[(r['model_label'],r['condition'])].append(r)
 summaries=[]
 for (m,c),rs in sorted(groups.items()):
  norms=[r['normalized'] for r in rs]
  qs=[q for n in norms for q in n['questions'] if q]
  # Distinguish generated candidates from ideas actually retained by each agent.
  # This matters for the V2 alternative: best-K may shift selection toward safer ideas
  # even if the full candidate set does not become more homogeneous.
  selected_qs=[
    str(n['ideas'][i-1].get('question',''))
    for n in norms
    for i in n.get('selected_ids',[])
    if isinstance(i,int) and 1<=i<=len(n.get('ideas',[]))
    and isinstance(n['ideas'][i-1],dict)
  ]
  acts=Counter(n['priority_action'] for n in norms)
  denom=sum(1 for r in rows if r['model_label']==m and r['condition']==c)
  summaries.append({'model':m,'condition':c,'n':len(rs),'valid_rate':len(rs)/denom if denom else 0,'mean_portfolio':mean([n['portfolio_size'] for n in norms]),'mean_verification_per_project':mean([n['verification_per_project'] for n in norms]),'idea_jaccard':pair(qs),'selected_idea_jaccard':pair(selected_qs),'submit_now_rate':acts['submit_now']/len(norms),'verify_more_rate':acts['verify_more']/len(norms),'reposition_rate':acts['reposition']/len(norms),'abandon_rate':acts['abandon']/len(norms),'mean_revised_verification':mean([n['revised_verification'] for n in norms])})
 cross=[]; models=sorted(set(r['model_label'] for r in valid))
 if len(models)>=2:
  for c in sorted(set(r['condition'] for r in valid)):
   q0=[q for r in valid if r['model_label']==models[0] and r['condition']==c for q in r['normalized']['questions'] if q]
   q1=[q for r in valid if r['model_label']==models[1] and r['condition']==c for q in r['normalized']['questions'] if q]
   vals=[jac(x,y) for x in q0 for y in q1]
   cross.append({'condition':c,'model_a':models[0],'model_b':models[1],'cross_family_jaccard':mean(vals)})
 contrasts=[]
 for m in models:
  d={x['condition']:x for x in summaries if x['model']==m}
  if 'quantity' in d and 'best_k' in d:
   contrasts.append({'model':m,'contrast':'best_k-minus-quantity','portfolio_diff':d['best_k']['mean_portfolio']-d['quantity']['mean_portfolio'],'verification_diff':d['best_k']['mean_verification_per_project']-d['quantity']['mean_verification_per_project'],'idea_overlap_diff':d['best_k']['idea_jaccard']-d['quantity']['idea_jaccard']})
  if 'quantity' in d and 'high_priority' in d:
   contrasts.append({'model':m,'contrast':'high_priority-minus-quantity','submit_now_diff':d['high_priority']['submit_now_rate']-d['quantity']['submit_now_rate'],'verify_more_diff':d['high_priority']['verify_more_rate']-d['quantity']['verify_more_rate'],'revised_verification_diff':d['high_priority']['mean_revised_verification']-d['quantity']['mean_revised_verification']})
 (out/'benchmark_summary.json').write_text(json.dumps({'summaries':summaries,'cross_family':cross,'contrasts':contrasts},indent=2),encoding='utf-8')
 if summaries:
  with (out/'benchmark_summary.csv').open('w',newline='',encoding='utf-8') as f:
   w=csv.DictWriter(f,fieldnames=list(summaries[0]));w.writeheader();w.writerows(summaries)
 lines=['# Stage-1 open-weight benchmark','',f'Total trajectories: {len(rows)}; valid structured trajectories: {len(valid)} ({len(valid)/len(rows):.1%}).' if rows else 'No trajectories.','', '## Cell summaries','', '| Model | Condition | n | Portfolio | Verification/project | Candidate Jaccard | Selected Jaccard | Submit now | Verify more |', '|---|---|---:|---:|---:|---:|---:|---:|---:|']
 for x in summaries:lines.append(f"| {x['model']} | {x['condition']} | {x['n']} | {x['mean_portfolio']:.2f} | {x['mean_verification_per_project']:.1f} | {x['idea_jaccard']:.3f} | {x['selected_idea_jaccard']:.3f} | {x['submit_now_rate']:.2f} | {x['verify_more_rate']:.2f} |")
 lines+=['','## Cross-family overlap','']+[f"- {x['condition']}: cross-family Jaccard = {x['cross_family_jaccard']:.3f}" for x in cross]
 lines+=['','## Pre-specified contrasts','']+[f"- {json.dumps(x)}" for x in contrasts]
 lines+=['','## Interpretation boundary','','These are small-model synthetic trajectories. They demonstrate that the artifact runs on real open-weight LLMs and can reveal institution- and model-dependent behavior. They are not estimates of human researcher behavior and are not confirmatory evidence for the theory.']
 (out/'BENCHMARK_REPORT.md').write_text('\n'.join(lines),encoding='utf-8'); print('\n'.join(lines))
if __name__=='__main__':main()
