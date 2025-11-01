from pydantic import BaseModel, Field
from typing import List, Dict, Any

class SubTask(BaseModel):
    agent: str
    brief: str
    contraintes: List[str] = []
    livrables: List[str] = []
    criteres_succes: List[str] = []

class Brief(BaseModel):
    meta: Dict[str, Any] = Field(default_factory=dict)
    contexte: str = ""
    objectif: str = ""
    sous_taches: List[SubTask] = Field(default_factory=list)
    contraintes_globales: List[str] = Field(default_factory=list)
    citations_obligatoires: bool = True

class Evidence(BaseModel):
    text: str
    source: str  # e.g., "doc.pdf#p=12"

class OrchestratorResponse(BaseModel):
    brief: Brief
    evidence: List[Evidence] | List[Dict[str, Any]]
    draft: Dict[str, Any]
    verdict: Dict[str, Any]
