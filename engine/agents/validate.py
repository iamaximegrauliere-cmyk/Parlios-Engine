from typing import List
from engine.core.models import UARequest, Plan

CHECKLIST = [
    "La réponse couvre-t-elle l'objectif ?",
    "Les contraintes implicites sont-elles respectées ?",
    "Le ton/format/longueur conviennent-ils ?",
]

def validate_output(req: UARequest, plan: Plan, output: str, logs: List[str]) -> str:
    missing = [c for c in CHECKLIST if "?" in c]  # MVP: placeholder
    if missing:
        logs.append(f"validate: checklist={len(CHECKLIST)} ok (MVP)")
    return output
