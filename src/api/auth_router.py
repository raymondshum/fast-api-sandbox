from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from model.model import User
from model.schema import UserLogin, UserToken
from service.database import SessionLocal, get_db
from service.user_service import UserService
from util.auth_utils import AuthUtils

router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post("/login", response_model=UserToken)
def login(credentials: UserLogin, db: SessionLocal = Depends(get_db)):
    existing_user: User = UserService.get_user_by_email(db=db, email=credentials.email)
    if not existing_user:
        raise HTTPException(
            status_code=404, detail=f"Email is not registered: {credentials.email}"
        )
    if not AuthUtils.authenticate_user(credentials.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Authentication failed")
    encoded_token: str = AuthUtils.get_jwt(
        id=existing_user.id, email=existing_user.email, expires_in=timedelta(minutes=30)
    )
    return UserToken(access_token=encoded_token, type="bearer")
