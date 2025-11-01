from typing import List, Dict

AMBIG_CATEGORIES = [
    "longueur_non_precisee", "style_indefini", "contexte_manquant",
    "objectif_flou", "contraintes_absentes"
]

class ClarifierAgent:
    """
    Règle simple et déterministe pour garder le repo fonctionnel sans dépendances externes.
    Heuristique: si la demande est trop courte (< 12 mots) OU contient des termes vagues,
    générer 1-3 questions ciblées.
    """
    def __init__(self, max_questions: int = 3):
        self.max_questions = max_questions
        self.vague_terms = {"stratégie", "idée", "truc", "chose", "améliorer", "optimiser", "plan"}

    def analyze(self, prompt: str) -> Dict:
        words = prompt.strip().split()
        findings: List[str] = []
        if len(words) < 12:
            findings.append("objectif_flou")
        if any(t in prompt.lower() for t in self.vague_terms):
            findings.append("contexte_manquant")
        return {"is_clear": len(findings) == 0, "categories": findings}

    def ask(self, prompt: str) -> List[str]:
        result = self.analyze(prompt)
        if result["is_clear"]:
            return []
        questions: List[str] = []
        if "objectif_flou" in result["categories"]:
            questions.append("Quel est l'objectif exact (succès mesurable, échéance) ?")
        if "contexte_manquant" in result["categories"]:
            questions.append("Dans quel contexte/outils (ex: GitHub, n8n, Notion) et pour qui ?")
        if "contraintes_absentes" in result["categories"]:
            questions.append("Y a‑t‑il des contraintes (budget/ton/format/longueur) ?")
        return questions[: self.max_questions]
