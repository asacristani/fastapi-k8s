from datetime import date
from typing import Any
from beanie import PydanticObjectId
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator


class ClaimIn(BaseModel):
    policy_number: str
    claim_type: str
    description: str
    date_of_incident: date


class ClaimUpdate(BaseModel):
    policy_number: str | None = None
    claim_type: str | None = None
    description: str | None = None
    date_of_incident: date | None = None


class ClaimOut(BaseModel):
    id: Any = Field(...)
    policy_number: str
    claim_type: str
    description: str
    date_of_incident: date

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str | PydanticObjectId) -> str:
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return str(value)

    @field_serializer("id")
    def serialize_id(self, value: ObjectId, _info):
        return str(value)

    @field_serializer("date_of_incident")
    def serialize_date(self, value: date, _info):
        return value.isoformat()

    model_config = ConfigDict(from_attributes=True)
