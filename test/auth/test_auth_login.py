import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    await client.post(
        "/auth/signup", json={"email": "user@example.com", "password": "securepassword"}
    )

    response = await client.post(
        "/auth/login", json={"email": "user@example.com", "password": "securepassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_failure(client: AsyncClient):
    response = await client.post(
        "/auth/login", json={"email": "user@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_unauthorized(client: AsyncClient):
    response = await client.get("/auth/me")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_current_user_success(client: AsyncClient, test_user, create_token):
    headers = {"Authorization": f"Bearer {create_token}"}

    response = await client.get("/auth/me", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["_id"] == str(test_user.id)
    assert data["email"] == test_user.email
