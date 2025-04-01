import pytest


@pytest.mark.asyncio
async def test_create_claim_ok(client):
    token = "fake-token"
    payload = {
        "policy_number": "POL123456",
        "claim_type": "robo",
        "description": "Robo de vehículo",
        "date_of_incident": "2025-03-30",
    }

    response = await client.post(
        "/claims", headers={"Authorization": f"Bearer {token}"}, json=payload
    )

    assert response.status_code == 201
    data = response.json()
    assert data["policy_number"] == payload["policy_number"]
    assert data["claim_type"] == payload["claim_type"]


@pytest.mark.asyncio
async def test_create_claim_unauthenticated(client):
    payload = {
        "policy_number": "POL123456",
        "claim_type": "robo",
        "description": "Robo de vehículo",
        "date_of_incident": "2025-03-30",
    }

    response = await client.post("/claims", json=payload)

    assert response.status_code in (401, 403)
