from fastapi.testclient import TestClient

from backend.main import app


def test_app_imports() -> None:
    assert app.title == "Money Movement Application"


def test_root_serves_dashboard() -> None:
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "Money Movement" in response.text


def test_openapi_schema_builds() -> None:
    schema = app.openapi()

    assert schema["info"]["title"] == "Money Movement Application"
    assert "/" in schema["paths"]
    assert "/api/auth/register" in schema["paths"]
    assert "/api/transfers" in schema["paths"]


def test_api_health_response() -> None:
    with TestClient(app) as client:
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
