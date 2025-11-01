from fastapi import FastAPI
from pydantic import BaseModel
from engine.core.orchestrator import Orchestrator
from engine.core.models import UARequest, UAResponse

app = FastAPI(title="Parlios Engine")

@app.get("/health")
def health(): return {"ok": True}

@app.get("/ready")
def ready(): return {"ok": True, "engine": "parlios"}

@app.post("/run", response_model=UAResponse)
def run(req: UARequest):
    ork = Orchestrator()
    return ork.run(req)
