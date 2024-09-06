from fastapi.testclient import TestClient
from app.app import app  # Import the FastAPI app

client = TestClient(app)

def test_login():
    response = client.post("/api/login", json={"username": "testuser", "password": "password123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_add_value():
    token = "your_token_here"  # Replace with a valid token from the login response
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/api/add",
        headers=headers,
        json={"list_id": 1, "value": "test_value", "comment": "Adding test value"}
    )
    assert response.status_code == 200
    assert response.json() == {"status": "Added successfully"}