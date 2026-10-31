"""Offline checks for the Stage-1 V2 experimental protocol and analysis.

These are interface checks. They do not validate any behavioral mechanism.
"""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("run_stage1_benchmark", ROOT/"scripts"/"run_stage1_benchmark.py")
module=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

conditions=module.load_conditions(str(ROOT/"configs"/"stage1_conditions.yaml"))
assert list(conditions)==["quantity","best_k","high_priority"]
assert "TWO strongest" in conditions["best_k"]["evaluation"]
assert "first" in conditions["high_priority"]["priority"].lower()

corpus=[{"text":"Research collaboration and scientific ideas are shaped by evaluation rules."}]
prompt=module.build_prompt(corpus,conditions["best_k"])
assert "FOUR substantively distinct" in prompt
assert "100 points" in prompt
assert "TWO strongest" in prompt

def example(agent,selected):
    ideas=[
      {"id":1,"title":"Quality standards","question":"When does verification improve research quality?","mechanism":"Attention shapes validity."},
      {"id":2,"title":"Peer review","question":"How does congestion slow journal review?","mechanism":"Capacity limits screening."},
      {"id":3,"title":"Research priority","question":"Does priority pressure increase rushing?","mechanism":"Speed competes with checking."},
      {"id":4,"title":"Novelty","question":"Do output rewards reduce topic diversity?","mechanism":"Rules change selection."}
    ]
    parsed={"ideas":ideas,"selected_ids":selected,
            "verification":{str(k):100/len(selected) for k in selected},
            "priority_response":{"focal_id":selected[0],"action":"verify_more","reason":"Robustness matters.","revised_verification":55}}
    norm=module.normalize(parsed)
    assert norm is not None
    return {"model_label":"toy","condition":"quantity","agent":agent,"normalized":norm}

with tempfile.TemporaryDirectory() as td:
    tmp=Path(td)
    raw=tmp/"raw_traces.jsonl"
    raw.write_text("\n".join(json.dumps(r) for r in [example(0,[1]),example(1,[1,2])])+"\n",encoding="utf-8")
    out=tmp/"results"
    subprocess.run([sys.executable,str(ROOT/"scripts"/"analyze_stage1_benchmark.py"),
                    str(raw),"--out",str(out)],check=True,capture_output=True,text=True)
    data=json.loads((out/"benchmark_summary.json").read_text(encoding="utf-8"))
    item=data["summaries"][0]
    assert "selected_idea_jaccard" in item
    assert "idea_jaccard" in item
    assert item["selected_idea_jaccard"]>item["idea_jaccard"]
print("Stage-1 V2 offline checks passed")
