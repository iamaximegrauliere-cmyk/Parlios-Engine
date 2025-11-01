from ..schemas.models import Brief, SubTask
from ..memory.profile_store import ProfileStore

class BriefingAgent:
    def __init__(self, profile: ProfileStore):
        self.profile = profile

    def from_fuzzy(self, prompt: str) -> Brief:
        # Minimal deterministic shaping; replace with LLM call in production.
        st = [
            SubTask(agent="recherche", brief="Collecter 3-5 extraits sourcés pertinents."),
            SubTask(agent="production", brief="Rédiger une réponse structurée adaptée au profil.")
        ]
        return Brief(
            meta={"timestamp": "now"},
            contexte=prompt,
            objectif="Clarifier et répondre avec citations",
            sous_taches=st,
            contraintes_globales=["style aligné au profil", "citations obligatoires"],
            citations_obligatoires=True
        )
