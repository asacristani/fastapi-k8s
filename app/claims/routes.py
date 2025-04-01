from fastapi import APIRouter, Depends, HTTPException, status

from app.claims.schemas import ClaimIn, ClaimOut, ClaimUpdate
from app.claims.models import Claim
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/claims",
    tags=["claims"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "",
    response_model=ClaimOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new claim",
    description="Submit a new insurance claim. The claim will be associated with the authenticated user.",
    response_description="Details of the created claim",
)
async def create_claim(
    payload: ClaimIn,
    user: dict = Depends(get_current_user),
):
    """
    Create a new insurance claim with the provided information.
    """
    claim = await Claim.create(payload, user)
    return ClaimOut.model_validate(claim)


@router.get(
    "/{claim_id}",
    response_model=ClaimOut,
    summary="Retrieve a specific claim",
    description="Get details for a specific insurance claim by its ID. Only claims owned by the user are accessible.",
    response_description="Details of the requested claim",
)
async def get_claim(
    claim_id: str,
    user: dict = Depends(get_current_user),
):
    """
    Retrieve an individual claim by its ID.
    """
    claim = await Claim.get_by_id(claim_id, user)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return ClaimOut.model_validate(claim)


@router.get(
    "",
    response_model=list[ClaimOut],
    summary="List all claims",
    description="Retrieve all insurance claims submitted by the currently authenticated user.",
    response_description="A list of all claims owned by the user",
)
async def list_claims(user: dict = Depends(get_current_user)):
    """
    List all claims for the current user.
    """
    claims = await Claim.list_by_user(user)
    return [ClaimOut.model_validate(claim) for claim in claims]


@router.put(
    "/{claim_id}",
    response_model=ClaimOut,
    summary="Update an existing claim",
    description="Modify an existing claim using its ID. Only claims owned by the user can be updated.",
    response_description="Details of the updated claim",
)
async def update_claim(
    claim_id: str,
    payload: ClaimUpdate,
    user: dict = Depends(get_current_user),
):
    """
    Update specific fields of an existing claim.
    """
    claim = await Claim.get_by_id(claim_id, user)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    await claim.update_fields(payload)
    return ClaimOut.model_validate(claim)


@router.delete(
    "/{claim_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a claim",
    description="Remove a specific insurance claim by its ID. Only claims owned by the user can be deleted.",
)
async def delete_claim(
    claim_id: str,
    user: dict = Depends(get_current_user),
):
    """
    Delete an insurance claim by its ID.
    """
    claim = await Claim.get_by_id(claim_id, user)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    await claim.remove()
