from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
import requests

@dataclass
class UARequest:
    goal: str
    prefs: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ParliosClient:
    def __init__(self, base_url: str = "http://localhost:8080", api_key: Optional[str] = None, timeout: int = 60):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.api_key = api_key
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        h = {"Content-Type": "application/json"}
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        return h

    def health(self) -> bool:
        r = self.session.get(f"{self.base_url}/health", timeout=self.timeout)
        r.raise_for_status()
        return r.json().get("ok", True)

    def ready(self) -> bool:
        r = self.session.get(f"{self.base_url}/ready", timeout=self.timeout)
        r.raise_for_status()
        return r.json().get("ok", True)

    def run(self, req: UARequest) -> Dict[str, Any]:
        r = self.session.post(f"{self.base_url}/run", json=asdict(req), headers=self._headers(), timeout=self.timeout)
        r.raise_for_status()
        return r.json()
