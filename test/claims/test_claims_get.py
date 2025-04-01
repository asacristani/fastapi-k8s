import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_claim_ok(client: AsyncClient, test_db):
    token = "fake-token"
    payload = {
        "policy_number": "POL123456",
        "claim_type": "robo",
        "description": "Break-in at home",
        "date_of_incident": "2025-03-30",
    }

    create_resp = await client.post(
        "/claims", headers={"Authorization": f"Bearer {token}"}, json=payload
    )
    assert create_resp.status_code == 201
    claim_id = create_resp.json()["id"]

    get_resp = await client.get(
        f"/claims/{claim_id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["policy_number"] == payload["policy_number"]
    assert data["claim_type"] == payload["claim_type"]
    assert data["description"] == payload["description"]


@pytest.mark.asyncio
async def test_get_claim_not_found(client: AsyncClient):
    fake_id = "65f00dfb62f57c0b93a0dead"
    resp = await client.get(
        f"/claims/{fake_id}", headers={"Authorization": "Bearer fake-token"}
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_claim_unauthenticated(client: AsyncClient):
    fake_id = "65f00dfb62f57c0b93a0dead"
    resp = await client.get(f"/claims/{fake_id}")
    assert resp.status_code == 401
