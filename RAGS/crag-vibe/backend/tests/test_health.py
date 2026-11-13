from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check_returns_ok():
    response = client.get("/api/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert isinstance(body["openai_configured"], bool)
    assert body["indexed_chunks"] == 0


def test_health_never_exposes_the_api_key(monkeypatch):
    from app import config

    monkeypatch.setattr(config, "OPENAI_API_KEY", "sk-test-secret-value")
    response = client.get("/api/health")

    assert "sk-test-secret-value" not in response.text
