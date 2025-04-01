import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_delete_claim_ok(client: AsyncClient, test_db):
    # Preparación: crear un claim
    token = "fake-token"
    payload = {
        "policy_number": "POL9999",
        "claim_type": "robo",
        "description": "Robo en el garaje",
        "date_of_incident": "2025-03-30",
    }
    create_resp = await client.post(
        "/claims", headers={"Authorization": f"Bearer {token}"}, json=payload
    )
    assert create_resp.status_code == 201
    claim_id = create_resp.json()["_id"]

    # Ejecución: eliminar el claim
    delete_resp = await client.delete(
        f"/claims/{claim_id}", headers={"Authorization": f"Bearer {token}"}
    )

    # Aserción
    assert delete_resp.status_code == 204


@pytest.mark.asyncio
async def test_delete_claim_not_found(client: AsyncClient):
    # Ejecución: intentar eliminar un claim inexistente
    fake_id = "65f00dfb62f57c0b93a0dead"  # ID válido pero inexistente
    resp = await client.delete(
        f"/claims/{fake_id}", headers={"Authorization": "Bearer fake-token"}
    )

    # Aserción
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_claim_unauthenticated(client: AsyncClient):
    # Ejecución: intento sin autenticación
    fake_id = "65f00dfb62f57c0b93a0dead"
    resp = await client.delete(f"/claims/{fake_id}")

    # Aserción
    assert resp.status_code == 401
