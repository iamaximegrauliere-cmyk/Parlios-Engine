# Orchestrator Integration Guide

> Objectif: brancher des **agents concrets** (clarify, planner, research, writer, validator) sans casser votre code existant.
> Vous pouvez soit intégrer le code ci-dessous, soit adapter les imports à votre structure.

## 1) Imports (dans `engine/orchestrator.py` ou équivalent)
```python
from engine.agents import clarify as clarify_agent
from engine.agents import planner as planner_agent
from engine.agents import research as research_agent
from engine.agents import writer as writer_agent
from engine.agents import validator as validator_agent
```

## 2) Pipeline (exemple dans `Orchestrator.run`)
```python
def run(self, request: UARequest) -> UAResponse:
    # 1) Clarify
    c = clarify_agent.run(request.query, prefs=request.prefs)
    # 2) Plan
    plan = planner_agent.build(c.refined_query)
    # 3) Execute
    artifacts = {}
    for step in plan.steps:
        if step.agent == "research":
            artifacts["research"] = research_agent.run(step.input["query"], context={"assumptions": c.assumptions})
        elif step.agent == "writer":
            w = writer_agent.run(step.input.get("topic", c.refined_query), style=step.input.get("style","summary"), context=artifacts)
            artifacts["content"] = w["content"]
    # 4) Validate
    val = validator_agent.run(artifacts)
    # 5) Save memory (votre mécanisme existant)
    self._save_memory({
        "query": request.query,
        "refined_query": c.refined_query,
        "assumptions": c.assumptions,
        "plan": [s.__dict__ for s in plan.steps],
        "artifacts": artifacts,
        "validation": val
    }, session_id=request.session_id)

    return UAResponse(
        ok=val["ok"],
        content=artifacts.get("content",""),
        meta={"assumptions": c.assumptions, "validation": val, "plan": [s.__dict__ for s in plan.steps]}
    )
```

## 3) Sécuriser `/run` (facultatif mais recommandé)
Dans `app/main.py` (ou fichier FastAPI), ajoutez:
```python
from app.security import require_api_key

@app.post("/run", dependencies=[Depends(require_api_key)])
def run_endpoint(req: UARequest):
    return orchestrator.run(req)
```

Configurez le secret **PARLIOS_API_KEY** côté environnement (Actions/Runner/Prod).
Si `PARLIOS_API_KEY` n'est pas défini, la vérification est **désactivée**.