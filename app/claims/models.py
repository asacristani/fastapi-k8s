from __future__ import annotations
from datetime import date

from beanie import Document
from pydantic import BaseModel
from bson import ObjectId

from app.auth.models import User


class Claim(Document):
    policy_number: str
    claim_type: str
    description: str
    date_of_incident: date
    user_id: str

    class Settings:
        name = "claims"

    @classmethod
    async def create(cls, data: BaseModel, user: User) -> Claim:
        claim = cls(**data.model_dump(), user_id=str(user.id))
        await claim.insert()
        return claim

    @classmethod
    async def get_by_id(cls, claim_id: str, user: User) -> Claim | None:
        return await cls.find_one({"_id": ObjectId(claim_id), "user_id": str(user.id)})

    @classmethod
    async def list_by_user(cls, user: User) -> list[Claim]:
        return await cls.find({"user_id": str(user.id)}).to_list()

    async def update_fields(self, data: BaseModel) -> Claim:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(self, field, value)
        await self.save()
        return self

    async def remove(self) -> None:
        await self.delete()
