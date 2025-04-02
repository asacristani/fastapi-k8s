from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime


class User(Document):
    email: EmailStr = Field(..., description="Unique email address of the user")
    hashed_password: str = Field(..., description="Hashed password using bcrypt")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the user was created",
    )

    class Settings:
        name = "users"  # MongoDB collection name
