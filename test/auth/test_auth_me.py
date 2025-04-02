import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_current_user_success(client: AsyncClient, create_token: str):
    response = await client.get(
        "/auth/me", headers={"Authorization": f"Bearer {create_token}"}
    )
    assert response.status_code == 200
    assert "email" in response.json()
