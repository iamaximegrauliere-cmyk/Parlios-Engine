from fastapi import APIRouter
from pydantic import BaseModel
from ..orchestrator.brain import Orchestrator

router = APIRouter()
brain = Orchestrator()

class AskPayload(BaseModel):
    question: str
    profile_overrides: dict | None = None

@router.post("/ask")
def ask(payload: AskPayload):
    return brain.ask(payload.question, profile_overrides=payload.profile_overrides)

class BriefInput(BaseModel):
    prompt_fluide: str

@router.post("/brief")
def brief(payload: BriefInput):
    return brain.make_brief(payload.prompt_fluide)

class RunInput(BaseModel):
    brief: dict

@router.post("/run")
def run(payload: RunInput):
    return brain.run_brief(payload.brief)

class VerifyInput(BaseModel):
    brief: dict
    response: dict

@router.post("/verify")
def verify(payload: VerifyInput):
    return brain.verify(payload.brief, payload.response)

class ProfileEvent(BaseModel):
    event: str
    payload: dict | None = None

@router.post("/profile/event")
def profile_event(evt: ProfileEvent):
    return brain.profile_event(evt.event, evt.payload or {})
