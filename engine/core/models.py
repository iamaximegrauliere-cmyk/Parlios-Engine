from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class UserPrefs(BaseModel):
    tone: Optional[str] = None
    length: Optional[str] = None
    format: Optional[str] = None

class UARequest(BaseModel):
    goal: str = Field(..., description="Intention floue ou précise")
    context: Optional[str] = None
    prefs: Optional[UserPrefs] = None

class Step(BaseModel):
    name: str
    details: Dict[str, Any] = {}

class Plan(BaseModel):
    steps: List[Step]

class UAResponse(BaseModel):
    ok: bool
    clarifications: List[str] = []
    plan: Optional[Plan] = None
    output: Optional[str] = None
    logs: List[str] = []
