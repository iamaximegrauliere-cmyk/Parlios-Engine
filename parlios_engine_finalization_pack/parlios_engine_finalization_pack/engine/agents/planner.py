from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class PlanStep:
    id: str
    agent: str
    input: Dict[str, Any]

@dataclass
class Plan:
    objective: str
    steps: List[PlanStep] = field(default_factory=list)

def build(objective: str) -> Plan:
    # Minimal plan: research -> writer
    return Plan(
        objective=objective,
        steps=[
            PlanStep(id="s1", agent="research", input={"query": objective}),
            PlanStep(id="s2", agent="writer", input={"topic": objective, "style": "structured outline"}),
        ],
    )