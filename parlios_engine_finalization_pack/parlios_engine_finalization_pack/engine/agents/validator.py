from typing import Dict, Any

def run(artifacts: Dict[str, Any]) -> Dict[str, Any]:
    ok = True
    issues = []
    if not artifacts.get("content"):
        ok = False
        issues.append("Missing content from writer.")
    return {"ok": ok, "issues": issues}