from typing import Dict, Any

def run(query: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    # Placeholder: simulate research output
    return {
        "highlights": [
            f"Background on: {query}",
            "Key concepts: orchestration, memory, ChatOps",
            "Open questions: integration depth of agents, guardrails"
        ],
        "sources": ["internal:memory", "repo:prompts"]
    }