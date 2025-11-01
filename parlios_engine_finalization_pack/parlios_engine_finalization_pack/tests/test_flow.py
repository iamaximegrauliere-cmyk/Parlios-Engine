import os, json
import importlib

def test_stub_flow():
    clarify = importlib.import_module("engine.agents.clarify")
    planner = importlib.import_module("engine.agents.planner")
    research = importlib.import_module("engine.agents.research")
    writer = importlib.import_module("engine.agents.writer")
    validator = importlib.import_module("engine.agents.validator")

    c = clarify.run("Explique l'orchestration IA", prefs={"tone":"pro","length":"short","format":"markdown"})
    assert c.refined_query
    plan = planner.build(c.refined_query)
    artifacts = {}
    for s in plan.steps:
        if s.agent == "research":
            artifacts["research"] = research.run(s.input["query"])
        elif s.agent == "writer":
            w = writer.run(s.input["topic"], style=s.input["style"], context=artifacts)
            artifacts["content"] = w["content"]
    val = validator.run(artifacts)
    assert val["ok"] is True
    assert "content" in artifacts and artifacts["content"]