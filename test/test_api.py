import pytest
from httpx import AsyncClient, ASGITransport
from dataclasses import dataclass, field

from app.main import app
from base import init, run_async

run_async(init())

client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")

@dataclass
class User:
    full_name: str
    email: str
    password: str
    url: str
    access_token: str = field(default=None)
    key: str = field(default=None)

user = User(
    full_name="John Doe",
    email="johndoe@example.com",
    password="12345Aa@",
    url="https://google.com/"
)


@pytest.mark.asyncio
async def test_register_user():
    response = await client.post("/api/users/", json=user.__dict__)
    assert response.status_code == 201
    assert "user_id" in response.json()

#
@pytest.mark.asyncio
async def test_login_for_access_token():
    response = await client.post("/api/users/token", json=user.__dict__)
    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    user.access_token = response_data["access_token"]


@pytest.mark.asyncio
async def test_read_user():
    response = await client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {user.access_token}"}
    )
    assert response.status_code == 200
    response_data = response.json()
    assert "email" in response_data


@pytest.mark.asyncio
async def test_create_url_shortcut():
    response = await client.post(
        "/api/urls/",
        json={
            "url": user.url,
            "is_active": False
        },
        headers={
            "Authorization": f"Bearer {user.access_token}"
        }
    )
    assert response.status_code == 201
    response_data = response.json()
    assert "key" in response_data
    user.key = response_data["key"]


@pytest.mark.asyncio
async def test_deactivate_url_redirect():
    response = await client.get(user.key)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_url_shortcut():
    response = await client.put(
        "/api/urls/",
        json={
            "key": user.key,
            "is_active": True
        },
        headers={
            "Authorization": f"Bearer {user.access_token}"
        }
    )
    assert response.status_code == 200
    assert "url" in response.json()


@pytest.mark.asyncio
async def test_activate_url_redirect():
    response = await client.get(user.key)
    assert response.status_code == 307
    assert "Location" in response.headers
    assert response.headers["Location"] == user.url
