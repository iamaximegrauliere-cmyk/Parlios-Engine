from typing import Dict, Any

def run(topic: str, style: str = "summary", context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    bullets = [
        f"Topic: {topic}",
        "What it does: clarify → plan → execute → validate → memorize",
        "Why it helps: GitHub-native automation + persistent memory",
        "Next steps: connect effectors and guardrails"
    ]
    return {"content": "\n".join(f"- {b}" for b in bullets), "format": "markdown"}