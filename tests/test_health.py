"""Basic smoke tests for the backend API."""
from __future__ import annotations


def test_health_endpoint():
    """Verify the backend ``/health`` endpoint returns HTTP 200."""
    from fastapi.testclient import TestClient

    from backend.api.main import app

    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
