from typing import Dict, List

class MetaReflectAgent:
    """
    Score simple et explicable pour la démonstration:
    - structure (présence de puces/sections)
    - concision (longueur raisonnable)
    - citations (presence champ 'evidence' ou 'sources')
    """
    def __init__(self):
        pass

    def score(self, response: Dict) -> Dict:
        txt = ""
        if isinstance(response, dict):
            txt = response.get("answer","")
        elif isinstance(response, str):
            txt = response
        else:
            txt = str(response)

        has_structure = ("- " in txt) or ("

" in txt)
        length = len(txt.split())
        concision_ok = 15 <= length <= 400
        ev = response.get("evidence", []) if isinstance(response, dict) else []
        citations_ok = bool(ev)

        subscores = {
            "structure": 1.0 if has_structure else 0.5,
            "concision": 1.0 if concision_ok else 0.6,
            "citations": 1.0 if citations_ok else 0.3
        }
        overall = round((subscores["structure"] + subscores["concision"] + subscores["citations"]) / 3, 2)
        notes: List[str] = []
        if not has_structure: notes.append("Ajoute des sections ou des puces.")
        if not concision_ok: notes.append("Ajuste la longueur (15-400 mots).")
        if not citations_ok: notes.append("Ajoute des extraits/sources (citations).")
        return {"score": overall, "subscores": subscores, "notes": notes}
