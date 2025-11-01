from engine.core.models import UARequest
from engine.core.orchestrator import Orchestrator

def test_pipeline_end_to_end():
    req = UARequest(goal="Synthétiser mes recherches", context="Parlios", prefs=None)
    res = Orchestrator().run(req)
    assert res.ok and res.plan and res.output
