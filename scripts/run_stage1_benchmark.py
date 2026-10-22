from __future__ import annotations
import argparse, json, os, time, urllib.request
from pathlib import Path

CONDITIONS={
 'quantity': {
   'evaluation': 'Your performance is evaluated broadly: each additional publishable project can improve your standing.',
   'priority': 'Priority matters, but independently valuable follow-on work still receives meaningful credit.'
 },
 'best_k': {
   'evaluation': 'Only your TWO strongest completed projects will count in evaluation. Extra projects beyond the best two carry no direct evaluation credit.',
   'priority': 'Priority matters, but independently valuable follow-on work still receives meaningful credit.'
 },
 'high_priority': {
   'evaluation': 'Your performance is evaluated broadly: each additional publishable project can improve your standing.',
   'priority': 'Being first is strongly rewarded. If a competing team publishes a substantially similar result first, the career value of your project falls sharply.'
 }
}

def load_corpus(path: Path):
    return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]

def build_prompt(corpus, condition):
    c='\n'.join(f"- {x['text']}" for x in corpus)
    return f"""You are an independent research team participating in a synthetic organizational-science laboratory. This is a research-design exercise, not advice about real misconduct. Use only the conceptual seed material below; do not invent citations.

SEED MATERIAL:
{c}

INSTITUTIONAL EVALUATION RULE:
{condition['evaluation']}

SCIENTIFIC PRIORITY RULE:
{condition['priority']}

You have a fixed HUMAN VERIFICATION BUDGET of 100 points.

Complete all four tasks:
1. Generate exactly FOUR substantively distinct research ideas. Each idea needs a short title, research question, and one-sentence mechanism.
2. Select the subset of ideas you would actually pursue under the evaluation rule. You may select 1 to 4.
3. Allocate exactly 100 verification points across ONLY the selected ideas. More points mean more human checking, robustness work, and scrutiny.
4. Now suppose you learn that another team is close to submitting a related result for your highest-priority selected idea. Choose one response: submit_now, verify_more, reposition, or abandon. State briefly why, and report how many verification points you would want on that focal idea after learning about the competitor (0-100).

Return JSON ONLY with this schema:
{{
  "ideas": [{{"id":1,"title":"...","question":"...","mechanism":"..."}}, ... exactly 4],
  "selected_ids": [1,2],
  "verification": {{"1":60,"2":40}},
  "priority_response": {{"focal_id":1,"action":"submit_now","reason":"...","revised_verification":45}}
}}
"""

def call(base_url, model, text, seed, timeout=240):
    payload={
      'model':model,
      'messages':[{'role':'user','content':text}],
      'temperature':0.35,
      'seed':seed,
      'max_tokens':650,
      'response_format':{'type':'json_object'}
    }
    req=urllib.request.Request(base_url.rstrip('/')+'/chat/completions', data=json.dumps(payload).encode(), headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        obj=json.loads(r.read().decode())
    return obj['choices'][0]['message']['content']

def parse_json(raw):
    try: return json.loads(raw), None
    except Exception as e1:
        try:
            a,b=raw.find('{'),raw.rfind('}')
            if a>=0 and b>a: return json.loads(raw[a:b+1]), 'extracted'
        except Exception as e2: return None, f'{type(e1).__name__};{type(e2).__name__}'
        return None, type(e1).__name__

def normalize(obj):
    if not isinstance(obj,dict): return None
    ideas=obj.get('ideas'); selected=obj.get('selected_ids'); ver=obj.get('verification',{}); pr=obj.get('priority_response',{})
    if not isinstance(ideas,list) or len(ideas)<1 or not isinstance(selected,list): return None
    ids=[]
    for x in selected:
        try: ids.append(int(x))
        except: pass
    ids=[i for i in ids if 1<=i<=len(ideas)]; ids=list(dict.fromkeys(ids))
    if not ids: return None
    vals=[]
    for i in ids:
        try: vals.append(max(0.0,float(ver.get(str(i),ver.get(i,0)))))
        except: vals.append(0.0)
    s=sum(vals); vals=([100.0/len(ids)]*len(ids)) if s<=0 else [v*100.0/s for v in vals]
    questions=[str(x.get('question','')).strip() if isinstance(x,dict) else str(x) for x in ideas]
    action=str(pr.get('action','')).strip().lower()
    if action not in {'submit_now','verify_more','reposition','abandon'}: action='other'
    try: revised=float(pr.get('revised_verification',0))
    except: revised=0.0
    return {
      'ideas':ideas,'questions':questions,'selected_ids':ids,
      'allocations':dict(zip([str(i) for i in ids],vals)),
      'portfolio_size':len(ids),'verification_per_project':100.0/len(ids),
      'priority_action':action,'revised_verification':max(0,min(100,revised)),
      'priority_reason':str(pr.get('reason',''))
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--base-url',default=os.environ.get('SUA_BASE_URL','http://127.0.0.1:8080/v1'))
    p.add_argument('--model',required=True); p.add_argument('--model-label',required=True)
    p.add_argument('--n-seeds',type=int,default=3); p.add_argument('--n-agents',type=int,default=6)
    p.add_argument('--out',required=True); p.add_argument('--corpus',default='data/seed_corpus.jsonl')
    p.add_argument('--commit',default=os.environ.get('GITHUB_SHA','unknown'))
    a=p.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True); corpus=load_corpus(Path(a.corpus)); traces=[]
    for cond_name,cond in CONDITIONS.items():
      for seed_ix in range(a.n_seeds):
       for agent in range(a.n_agents):
        seed=20261021+seed_ix*1000+agent; txt=build_prompt(corpus,cond); t=time.time()
        try: raw=call(a.base_url,a.model,txt,seed); err=None
        except Exception as e: raw=''; err=f'{type(e).__name__}: {e}'
        parsed,parse_note=parse_json(raw) if raw else (None,None); norm=normalize(parsed) if parsed else None
        traces.append({'model_label':a.model_label,'model_request':a.model,'condition':cond_name,'seed_index':seed_ix,'seed':seed,'agent':agent,'commit_sha':a.commit,'elapsed_sec':round(time.time()-t,3),'prompt':txt,'raw_response':raw,'call_error':err,'parse_note':parse_note,'parsed':parsed,'normalized':norm})
        print(a.model_label,cond_name,seed_ix,agent,'OK' if norm else 'INVALID',round(time.time()-t,1),flush=True)
    with (out/'raw_traces.jsonl').open('w',encoding='utf-8') as f:
      for x in traces:f.write(json.dumps(x,ensure_ascii=False)+'\n')
    manifest={'model_label':a.model_label,'model_request':a.model,'n_seeds':a.n_seeds,'n_agents':a.n_agents,'conditions':list(CONDITIONS),'commit_sha':a.commit,'trajectory_count':len(traces),'valid_count':sum(x['normalized'] is not None for x in traces)}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps(manifest,indent=2))
if __name__=='__main__':main()
