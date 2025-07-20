import pytest

@pytest.mark.asyncio
async def test_register_user(async_client, user_data):
    """Test successful user registration."""
    response = await async_client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201, "User registration should return 201."
    assert response.json()["email"] == user_data["email"], "Registered email should match."

@pytest.mark.asyncio
async def test_register_duplicate_user(async_client, user_data, create_user):
    """Test duplicate user registration returns 400."""
    response = await async_client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400, "Duplicate registration should return 400."
    assert "already registered" in response.text, "Error message should mention already registered."

@pytest.mark.asyncio
async def test_login_user(async_client, user_data, create_user):
    """Test successful login returns access token."""
    response = await async_client.post(
        "/api/v1/auth/token",
        data={"username": user_data["email"], "password": user_data["password"]},
    )
    assert response.status_code == 200, "Login should return 200."
    assert "access_token" in response.json(), "Response should contain access_token."

@pytest.mark.asyncio
async def test_login_wrong_password(async_client, user_data, create_user):
    """Test login with wrong password returns 401."""
    response = await async_client.post(
        "/api/v1/auth/token",
        data={"username": user_data["email"], "password": "wrongpass"},
    )
    assert response.status_code == 401, "Wrong password should return 401."
    assert "Incorrect email or password" in response.text, "Error message should mention incorrect credentials."

@pytest.mark.asyncio
async def test_get_current_user(async_client, user_token):
    """Test getting current user with valid token."""
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200, "Should return 200 for valid token."
    assert "email" in response.json(), "Response should contain email."

@pytest.mark.asyncio
async def test_get_current_user_unauthenticated(async_client):
    """Test getting current user without token returns 401."""
    response = await async_client.get("/api/v1/auth/me")
    assert response.status_code == 401, "No token should return 401."
