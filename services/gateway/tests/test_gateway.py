"""Gateway smoke tests (no upstream required for /health)."""

from fastapi.testclient import TestClient

from gateway_service.main import create_app


def test_live() -> None:
    with TestClient(create_app()) as client:
        r = client.get("/health/live")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


def test_root() -> None:
    with TestClient(create_app()) as client:
        r = client.get("/")
        assert r.status_code == 200
        assert r.json()["service"] == "ams-gateway"


def test_unknown_path() -> None:
    with TestClient(create_app()) as client:
        r = client.get("/api/v1/unknown-resource")
        assert r.status_code == 404
