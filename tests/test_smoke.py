from pathlib import Path
import json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(ROOT/'scripts'/'run_demo.py')], check=True, capture_output=True, text=True)

def load(name):
    return json.loads((ROOT/'sample_results'/name/'summary.json').read_text())

b=load('baseline'); q=load('high_ai_quantity'); k=load('high_ai_bestk')
assert q['primary_projects'] > b['primary_projects']
assert q['avg_verification'] < b['avg_verification']
assert q['total_submissions'] > b['total_submissions']
assert k['primary_projects'] < q['primary_projects']
assert k['avg_verification'] > q['avg_verification']
for name in ['baseline','high_ai_quantity','high_ai_bestk']:
    assert (ROOT/'sample_results'/name/'traces.jsonl').exists()
    assert (ROOT/'sample_results'/name/'run_metadata.json').exists()
print('smoke tests passed')
