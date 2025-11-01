from typing import List
from engine.core.models import UARequest, UAResponse, Plan, Step
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
        logs.append(f"plan: {plan.json() if plan else None}")
        output = self._execute(plan, req)
        logs.append("execute: done")
        output = validate_output(req, plan, output, logs)
        self.mem.save_session(req, plan, output)
        return UAResponse(ok=True, clarifications=clarifs, plan=plan, output=output, logs=logs)

    def _execute(self, plan: Plan, req: UARequest) -> str:
        parts = [f"- {s.name}" for s in plan.steps] if plan else ["(no plan)"]
        style = f"(tone={req.prefs.tone})" if req.prefs and req.prefs.tone else ""
        return f"Objectif: {req.goal}\n{style}\nPlan:\n" + "\n".join(parts)
