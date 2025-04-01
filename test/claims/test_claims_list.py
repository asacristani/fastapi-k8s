import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_claims_ok(client: AsyncClient, test_db):
    token = "fake-token"
    payload_1 = {
        "policy_number": "POL1001",
        "claim_type": "accidente",
        "description": "Rear-end collision",
        "date_of_incident": "2025-03-15",
    }
    payload_2 = {
        "policy_number": "POL1002",
        "claim_type": "robo",
        "description": "Bike stolen",
        "date_of_incident": "2025-03-20",
    }

    await client.post(
        "/claims", headers={"Authorization": f"Bearer {token}"}, json=payload_1
    )
    await client.post(
        "/claims", headers={"Authorization": f"Bearer {token}"}, json=payload_2
    )

    resp = await client.get("/claims", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # at least the two created claims
    policy_numbers = [claim["policy_number"] for claim in data]
    assert "POL1001" in policy_numbers
    assert "POL1002" in policy_numbers


@pytest.mark.asyncio
async def test_list_claims_unauthenticated(client: AsyncClient):
    resp = await client.get("/claims")
    assert resp.status_code == 401
