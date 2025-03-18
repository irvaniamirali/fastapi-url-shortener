from fastapi.testclient import TestClient

from app.main import app
from test.base import init, run_async

# initialize the database
run_async(init())

client = TestClient(app=app)

user_data = {
    "full_name": "User Name",
    "email": "3345342user@example.com",
    "password": "The1234@"
}

def test_create_user():
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 201
    user_info = response.json()
    user_data["user_id"] = user_info["user_id"]

def test_login_for_access_token():
    response = client.post("/api/users/token", json=user_data)
    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    user_data["access_token"] = response_data["access_token"]

def test_read_user():
    access_token = user_data.get("access_token")
    response = client.get(
        "/api/users/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    assert response.status_code == 200
    user_info = response.json()
    assert "email" in user_info
