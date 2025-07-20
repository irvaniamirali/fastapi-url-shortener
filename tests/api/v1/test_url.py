import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_url(async_client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    data = {"original_url": "https://example.com"}
    response = await async_client.post("/api/v1/url/", json=data, headers=headers)
    assert response.status_code == 201
    assert response.json()["original_url"].rstrip("/") == "https://example.com".rstrip("/")
    assert "short_code" in response.json()

@pytest.mark.asyncio
async def test_create_url_custom_code(async_client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    data = {"original_url": "https://example.com", "custom_short_code": "custom123"}
    response = await async_client.post("/api/v1/url/", json=data, headers=headers)
    assert response.status_code == 201
    assert response.json()["short_code"] == "custom123"

@pytest.mark.asyncio
async def test_create_url_duplicate_custom_code(async_client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    data = {"original_url": "https://example.com", "custom_short_code": "dupe123"}
    await async_client.post("/api/v1/url/", json=data, headers=headers)
    response = await async_client.post("/api/v1/url/", json=data, headers=headers)
    assert response.status_code == 400
    assert "already in use" in response.text

@pytest.mark.asyncio
async def test_list_user_urls(async_client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.get("/api/v1/url/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_url_by_id(async_client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    # Create URL
    data = {"original_url": "https://getid.com"}
    create_resp = await async_client.post("/api/v1/url/", json=data, headers=headers)
    url_id = create_resp.json()["id"]
    # Get URL
    response = await async_client.get(f"/api/v1/url/{url_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == url_id

@pytest.mark.asyncio
async def test_update_url(async_client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    data = {"original_url": "https://update.com"}
    create_resp = await async_client.post("/api/v1/url/", json=data, headers=headers)
    url_id = create_resp.json()["id"]
    update_data = {"original_url": "https://updated.com"}
    response = await async_client.put(f"/api/v1/url/{url_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["original_url"].rstrip("/") == "https://updated.com".rstrip("/")

@pytest.mark.asyncio
async def test_delete_url(async_client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    data = {"original_url": "https://delete.com"}
    create_resp = await async_client.post("/api/v1/url/", json=data, headers=headers)
    url_id = create_resp.json()["id"]
    response = await async_client.delete(f"/api/v1/url/{url_id}", headers=headers)
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_get_url_analytics(async_client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    data = {"original_url": "https://analytics.com"}
    create_resp = await async_client.post("/api/v1/url/", json=data, headers=headers)
    url_id = create_resp.json()["id"]
    response = await async_client.get(f"/api/v1/url/{url_id}/analytics", headers=headers)
    assert response.status_code == 200
    assert "total_clicks" in response.json()

@pytest.mark.asyncio
async def test_get_qr_code(async_client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    data = {"original_url": "https://qr.com"}
    create_resp = await async_client.post("/api/v1/url/", json=data, headers=headers)
    url_id = create_resp.json()["id"]
    response = await async_client.get(f"/api/v1/url/{url_id}/qr", headers=headers)
    assert response.status_code == 200
    assert "qr_code_png_base64" in response.json()
