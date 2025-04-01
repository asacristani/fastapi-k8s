import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_update_claim_ok(client: AsyncClient, test_db):
    token = "fake-token"
    payload = {
        "policy_number": "POL9999",
        "claim_type": "robo",
        "description": "Initial description",
        "date_of_incident": "2025-03-10",
    }

    create_resp = await client.post(
        "/claims", headers={"Authorization": f"Bearer {token}"}, json=payload
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    claim_id = created["id"]

    update_data = {"description": "Updated description"}

    update_resp = await client.put(
        f"/claims/{claim_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=update_data,
    )
    assert update_resp.status_code == 200

    updated = update_resp.json()
    assert updated["description"] == "Updated description"
    assert updated["policy_number"] == payload["policy_number"]
    assert updated["claim_type"] == payload["claim_type"]


@pytest.mark.asyncio
async def test_update_claim_unauthenticated(client: AsyncClient):
    update_data = {"description": "This should not succeed"}

    resp = await client.put("/claims/123456", json=update_data)
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_update_claim_not_found(client: AsyncClient):
    token = "fake-token"
    fake_id = "65f00dfb62f57c0b93a0dead"
    update_data = {"description": "Doesn't matter"}

    resp = await client.put(
        f"/claims/{fake_id}",
        headers={"Authorization": f"Bearer {token}"},
        json=update_data,
    )
    assert resp.status_code == 404
