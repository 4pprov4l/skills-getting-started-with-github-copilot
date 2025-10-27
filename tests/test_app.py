import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.post(f"/activities/{activity}/unregister", json={"email": email})
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Try duplicate signup
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    # Clean up
    client.post(f"/activities/{activity}/unregister", json={"email": email})


def test_unregister_participant():
    email = "testuser2@mergington.edu"
    activity = "Chess Club"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/unregister", json={"email": email})
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]
    # Try to remove again
    response_dup = client.post(f"/activities/{activity}/unregister", json={"email": email})
    assert response_dup.status_code == 400
