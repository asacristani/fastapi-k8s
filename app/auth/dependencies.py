from fastapi import Header, HTTPException, status


async def get_current_user(authorization: str = Header(default=None)) -> dict[str, any]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    # TODO: Implement JWT decoding. Now we return a fake user. All the tokens are valid.
    return {"id": "test-user"}
