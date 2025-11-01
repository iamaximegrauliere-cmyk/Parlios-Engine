from typing import List
from engine.core.models import UARequest

def clarify(req: UARequest) -> List[str]:
    q = []
    if len(req.goal.strip()) < 12:
        q.append("Peux-tu préciser l'objectif (portée, public, contrainte de temps) ?")
    if not req.prefs or not (req.prefs.tone or req.prefs.format or req.prefs.length):
        q.append("As-tu des préférences de ton/format/longueur ?")
    return q
