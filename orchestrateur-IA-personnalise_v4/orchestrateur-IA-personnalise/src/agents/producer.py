from ..schemas.models import Brief, Evidence
from ..memory.profile_store import ProfileStore

class ProducerAgent:
    def __init__(self, profile: ProfileStore):
        self.profile = profile

    def produce(self, brief: Brief, evidence):
        style = self.profile.current_style()
        return {
            "answer": f"[{style['ton']}] Réponse de démonstration basée sur {len(evidence)} extrait(s).",
            "evidence": [e.model_dump() if hasattr(e, "model_dump") else e for e in evidence]
        }
