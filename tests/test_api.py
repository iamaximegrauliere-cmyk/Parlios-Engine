from fastapi.testclient import TestClient
from engine.api.main import app

c = TestClient(app)

def test_health():
    assert c.get("/health").json()["ok"] is True

def test_run_minimal():
    payload = {"goal": "Faire un plan"}
    r = c.post("/run", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert "plan" in data
