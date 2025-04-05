from fastapi.testclient import TestClient

from app.main import app
from test.base import init, run_async

# initialize the database
run_async(init())

client = TestClient(app=app)

user_data = {
    "full_name": "User Name",
    "email": "user@example.com",
    "password": "Pass1234@"
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

def test_create_url_shortcut():
    access_token = user_data.get("access_token")
    response = client.post(
        "/api/urls",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"url": "https://google.com/"}
    )
    assert response.status_code == 201
    response_data = response.json()
    assert "key" in response_data
    user_data["url_key"] = response_data["key"]

def test_create_url_shortcut_with_invalid_token():
    invalid_access_token = "invalid_token"
    response = client.post(
        "/api/urls",
        headers={"Authorization": f"Bearer {invalid_access_token}"},
        json={"url": "https://google.com/"}
    )
    assert response.status_code == 401
    assert response.json().get("detail") == "Could not validate credentials"

def test_update_url_shortcut():
    access_token = user_data.get("access_token")
    response = client.put(
        "/api/urls",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"url": "https://github.com/", "key": user_data["url_key"]}
    )
    assert response.status_code == 200
    assert "key" in response.json()

def test_update_url_shortcut_with_invalid_key():
    access_token = user_data.get("access_token")
    response = client.put(
        "/api/urls",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"url": "https://github.com/", "key": "abcdef"}
    )
    assert response.status_code == 404
    assert response.json().get("detail") == "This URL is not found or the provided key is invalid."

def test_redirect_url_shortcut():
    response = client.get(user_data["url_key"])
    assert response.status_code == 200

def test_redirect_url_shortcut_with_invalid_key():
    response = client.get("abcdef")
    assert response.status_code == 404
    assert response.json().get("detail") == "This URL Key does not exist."
