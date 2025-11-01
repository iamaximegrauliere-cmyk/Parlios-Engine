from ..schemas.models import Brief

class VerifierAgent:
    def check(self, brief: Brief, draft, evidence):
        has_sources = bool(evidence)
        ok = has_sources if brief.citations_obligatoires else True
        return {
            "citations_presentes": has_sources,
            "conforme": ok,
            "notes": "Vérification minimale (remplacer par critères du brief)."
        }
