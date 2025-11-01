from engine.core.models import UARequest, Plan, Step

def make_plan(req: UARequest, clarifs):
    steps = [
        Step(name="Analyser la demande et les clarifications"),
        Step(name="Structurer un brief (objectifs, livrables, critères de succès)"),
        Step(name="Produire le livrable initial"),
        Step(name="Auto-vérification/checklist et amélioration"),
    ]
    return Plan(steps=steps)
