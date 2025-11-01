# Parlios Engine – cURL Cheat Sheet

> Remplacez `http://localhost:8080` par l'URL de votre déploiement.

## Health
```bash
curl -s http://localhost:8080/health | jq .
curl -s http://localhost:8080/ready | jq .
curl -s -X POST http://localhost:8080/run \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Rédige un plan d'\''article sur l’orchestration IA.",
    "prefs": {"tone":"pro","length":"short","format":"markdown"},
    "session_id": "demo-001"
  }' | jq .
curl -s -X POST http://localhost:8080/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PARLIOS_API_KEY" \
  -d '{
    "goal": "Synthétise les points clés de la dernière session.",
    "prefs": {"tone":"neutral","length":"medium"},
    "session_id": "demo-002"
  }' | jq .

---

# 5) `engine/core/orchestrator.py` — no warnings (Pydantic v2)
```python
from typing import List
from engine.core.models import UARequest, UAResponse, Plan
from engine.agents.clarify import clarify
from engine.agents.plan import make_plan
from engine.agents.validate import validate_output
from engine.memory.store import Memory

class Orchestrator:
    def __init__(self):
        self.mem = Memory()

    def run(self, req: UARequest) -> UAResponse:
        logs: List[str] = []
        clarifs = clarify(req)
        logs.append(f"clarify: {clarifs}")
        plan = make_plan(req, clarifs)
        # Pydantic v2 : model_dump_json() au lieu de .json()
        logs.append(f"plan: {plan.model_dump_json() if plan else None}")
        output = self._execute(plan, req)
        logs.append("execute: done")
        output = validate_output(req, plan, output, logs)
        self.mem.save_session(req, plan, output)
        return UAResponse(ok=True, clarifications=clarifs, plan=plan, output=output, logs=logs)

    def _execute(self, plan: Plan, req: UARequest) -> str:
        parts = [f"- {s.name}" for s in plan.steps] if plan else ["(no plan)"]
        style = f"(tone={req.prefs.tone})" if req.prefs and req.prefs.tone else ""
        return f"Objectif: {req.goal}\n{style}\nPlan:\n" + "\n".join(parts)
