from pathlib import Path
import json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(ROOT/'scripts'/'run_demo.py')], check=True, capture_output=True, text=True)

def load(name):
    return json.loads((ROOT/'sample_results'/name/'summary.json').read_text())

b=load('baseline'); q=load('high_ai_quantity'); k=load('high_ai_bestk')
assert q['primary_projects'] > b['primary_projects']
assert q['avg_verification'] < b['avg_verification']
assert q['idea_overlap_jaccard'] > b['idea_overlap_jaccard']
assert q['total_submissions'] > b['total_submissions']
assert k['primary_projects'] < q['primary_projects']
assert k['avg_verification'] > q['avg_verification']
print('smoke tests passed')
