import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from configs import HOST, PORT

BASE_URL = f"http://{HOST}:{PORT}/"

client = AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL)

@pytest.mark.anyio
async def test_root():
    response = await client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
