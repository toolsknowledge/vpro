def test_health_reports_status_without_secrets(client, settings):
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["openai_configured"] is True
    assert body["chat_model"] == settings.openai_chat_model
    assert body["vector_store"] == {
        "ready": True,
        "collection_name": "test_collection",
        "chunk_count": 0,
        "error": None,
    }
    assert "sk-test-not-a-real-key" not in response.text


def test_health_works_without_api_key(client, make_settings):
    from config import get_settings
    from main import app

    app.dependency_overrides[get_settings] = lambda: make_settings(openai_api_key="")
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["openai_configured"] is False


def test_unknown_route_uses_error_shape(client):
    response = client.get("/api/does-not-exist")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "http_error"
