import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app

client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")

@pytest.mark.anyio
async def test_root():
    response = await client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
