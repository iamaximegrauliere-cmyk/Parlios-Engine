from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ClarifyResult:
    refined_query: str
    assumptions: Dict[str, Any]

def run(query: str, prefs: Dict[str, Any] | None = None) -> ClarifyResult:
    # Minimal heuristic clarification
    refined = query.strip()
    assumptions = {}
    if prefs:
        assumptions["tone"] = prefs.get("tone")
        assumptions["length"] = prefs.get("length")
        assumptions["format"] = prefs.get("format")
    return ClarifyResult(refined_query=refined, assumptions=assumptions)