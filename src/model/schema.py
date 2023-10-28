from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    model_config = config
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str]
    last_name: Optional[str]


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    # access_token


class UserLogin(BaseModel):
    model_config = config
    email: EmailStr
    password: str
