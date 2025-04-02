from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, Field
from beanie import PydanticObjectId
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SignupSchema(BaseModel):
    email: EmailStr
    password: str


class LoginSchema(SignupSchema):
    pass


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    email: EmailStr

    class Config:
        populate_by_name = True


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def signup(data: SignupSchema):
    existing = await User.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = pwd_context.hash(data.password)
    user = User(email=data.email, hashed_password=hashed_pw)
    await user.insert()
    return user


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginSchema):
    user = await User.find_one({"email": data.email})
    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    now = datetime.utcnow()
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user.id), "exp": expire}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {"access_token": token}


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Returns the currently authenticated user's data.",
)
async def get_me(user: dict = Depends(get_current_user)):
    """
    Retrieve the current authenticated user's information.
    """
    return user
