from fastapi import FastAPI
from pydantic import BaseModel
from .routers import router as orchestrator_router

app = FastAPI(title="Orchestrateur IA personnalisé")

app.include_router(orchestrator_router)

class Health(BaseModel):
    status: str = "ok"

@app.get("/health", response_model=Health)
def health():
    return Health()
