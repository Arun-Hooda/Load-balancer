import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

import pytest
from app import create_app


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("SERVER_NAME", "Test Server")
    return create_app().test_client()


def test_home_returns_200(client):
    assert client.get("/").status_code == 200


def test_home_shows_server_name(client):
    assert b"Test Server" in client.get("/").data


def test_whoami_returns_json_with_server_name(client):
    resp = client.get("/api/whoami")
    assert resp.get_json() == {"server": "Test Server"}


def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_unknown_route_returns_404(client):
    assert client.get("/does-not-exist").status_code == 404
