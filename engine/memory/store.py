import json, os, time
from typing import Optional
from engine.core.models import UARequest, Plan

BASE = ".ua/memory"

class Memory:
    def __init__(self, base: str = BASE):
        os.makedirs(base, exist_ok=True)
        self.base = base

    def save_session(self, req: UARequest, plan: Optional[Plan], output: str):
        ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        path = os.path.join(self.base, f"session_{ts}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump({
                "ts": ts,
                "goal": req.goal,
                "prefs": (req.prefs.dict() if req.prefs else None),
                "plan": (plan.dict() if plan else None),
                "output": output
            }, f, ensure_ascii=False, indent=2)
