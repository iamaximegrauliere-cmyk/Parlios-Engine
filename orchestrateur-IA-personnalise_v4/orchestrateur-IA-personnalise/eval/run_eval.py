import json, sys, pathlib, time, statistics
from typing import List, Dict, Any
import requests

API = "http://localhost:8080/ask"

def run_eval(ds_path: str) -> Dict[str, Any]:
    ok, total = 0, 0
    latencies = []
    misses = []
    for line in open(ds_path, "r", encoding="utf-8"):
        if not line.strip(): 
            continue
        total += 1
        ex = json.loads(line)
        t0 = time.time()
        try:
            r = requests.post(API, json={"question": ex["question"]}, timeout=20)
            r.raise_for_status()
            data = r.json()
            ans = (data.get("draft", {}) or {}).get("answer", "")
            latencies.append(time.time() - t0)
            if ans and all(tok.lower() in ans.lower() for tok in ex.get("expected_contains", [])):
                ok += 1
            else:
                misses.append({"q": ex["question"], "got": ans[:300]})
        except Exception as e:
            misses.append({"q": ex["question"], "error": str(e)})
    return {
        "exactitude_simple": round(ok / max(1, total), 3),
        "latence_p50": round(statistics.median(latencies), 3) if latencies else None,
        "latence_p95": round(statistics.quantiles(latencies, n=100)[94], 3) if latencies else None,
        "misses": misses[:10]
    }

if __name__ == "__main__":
    ds = sys.argv[1] if len(sys.argv) > 1 else "eval/dataset.jsonl"
    report = run_eval(ds)
    pathlib.Path("docs/eval_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
