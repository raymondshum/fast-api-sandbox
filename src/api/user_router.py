from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr

from model.schema import UserCreate, UserResponse, UserToken, UserUpdate
from service.auth_service import AuthService
from service.database import SessionLocal, get_db
from service.user_service import UserService
from util.auth_utils import AuthUtils

router = APIRouter(prefix="/v1/user", tags=["user"])


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    existing_user = UserService.get_user_by_email(db=db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return UserService.create_user(db=db, user=user)


@router.get("/{email}", response_model=UserResponse)
def get_user(
    email: EmailStr,
    token: Annotated[UserToken, Depends(AuthUtils.get_token_from_header)],
    db: SessionLocal = Depends(get_db),
):
    if not AuthService.token_is_active(db=db, token=token):
        raise HTTPException(status_code=401, detail="User not logged in.")
    existing_user = UserService.get_user_by_email(db=db, email=email)
    if not existing_user:
        raise HTTPException(
            status_code=404, detail=f"User not found for email: {email}"
        )
    if not existing_user.validate_jwt(token):
        raise HTTPException(status_code=403, detail=f"User not authorized to resource.")
    return existing_user


@router.delete("/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    email: EmailStr,
    token: Annotated[UserToken, Depends(AuthUtils.get_token_from_header)],
    db: SessionLocal = Depends(get_db),
):
    if not AuthService.token_is_active(db=db, token=token):
        raise HTTPException(status_code=401, detail="User not logged in.")
    existing_user = UserService.get_user_by_email(db=db, email=email)
    if not existing_user:
        raise HTTPException(
            status_code=404, detail=f"User not found for email: {email}"
        )
    if not existing_user.validate_jwt(token):
        raise HTTPException(status_code=403, detail=f"User not authorized to resource.")
    existing_user = UserService.delete_user(db=db, user=existing_user)


@router.put("/{email}", response_model=UserResponse)
def update_user(
    email: EmailStr,
    updated_fields: UserUpdate,
    token: Annotated[UserToken, Depends(AuthUtils.get_token_from_header)],
    db: SessionLocal = Depends(get_db),
):
    if not AuthService.token_is_active(db=db, token=token):
        raise HTTPException(status_code=401, detail="User not logged in.")
    existing_user = UserService.get_user_by_email(db=db, email=email)
    if not existing_user:
        raise HTTPException(
            status_code=404, detail=f"User not found for email: {email}"
        )
    if not existing_user.validate_jwt(token):
        raise HTTPException(status_code=403, detail=f"User not authorized to resource.")
    return UserService.update_user(
        db=db, updated_fields=updated_fields, existing_user=existing_user
    )
