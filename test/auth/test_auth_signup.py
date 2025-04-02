import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_signup_success(client: AsyncClient):
    payload = {"email": "newuser@example.com", "password": "newsecurepassword"}

    response = await client.post("/auth/signup", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert "_id" in data


@pytest.mark.asyncio
async def test_signup_duplicate_email(client: AsyncClient):
    payload = {"email": "existinguser@example.com", "password": "any"}

    await client.post("/auth/signup", json=payload)

    response = await client.post("/auth/signup", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"
