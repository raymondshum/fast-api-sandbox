from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr

from model.schema import UserCreate, UserResponse, UserToken, UserUpdate
from service.database import SessionLocal, get_db
from service.user_service import UserService
from util.auth_utils import AuthUtils

router = APIRouter(prefix="/v1/user", tags=["user"])


@router.post("/user", response_model=UserResponse)
def create_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    existing_user = UserService.get_user_by_email(db=db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return UserService.create_user(db=db, user=user)


@router.get("/user/{email}", response_model=UserResponse)
def get_user(
    email: EmailStr,
    token: Annotated[UserToken, Depends(AuthUtils.get_token_from_header)],
    db: SessionLocal = Depends(get_db),
):
    existing_user = UserService.get_user_by_email(db=db, email=email)
    if not existing_user:
        raise HTTPException(
            status_code=404, detail=f"User not found for email: {email}"
        )
    return existing_user


@router.delete("/user/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(email: EmailStr, db: SessionLocal = Depends(get_db)):
    existing_user = UserService.get_user_by_email(db=db, email=email)
    if not existing_user:
        raise HTTPException(
            status_code=404, detail=f"User not found for email: {email}"
        )
    existing_user = UserService.delete_user(db=db, user=existing_user)


@router.put("/user/{email}", response_model=UserResponse)
def update_user(
    email: EmailStr, updated_fields: UserUpdate, db: SessionLocal = Depends(get_db)
):
    existing_user = UserService.get_user_by_email(db=db, email=email)
    if not existing_user:
        raise HTTPException(
            status_code=404, detail=f"User not found for email: {email}"
        )
    return UserService.update_user(
        db=db, updated_fields=updated_fields, existing_user=existing_user
    )
