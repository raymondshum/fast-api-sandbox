import logging
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from model.model import User
from model.schema import TokenCreate, UserLogin, UserToken, UserTokenResponse
from service.auth_service import AuthService
from service.database import SessionLocal, get_db
from service.user_service import UserService
from util.auth_utils import AuthUtils

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/auth", tags=["auth"])


@router.post("/login", response_model=UserTokenResponse)
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
    existing_token = AuthService.get_token_by_user_id(db=db, user_id=existing_user.id)
    if existing_token:
        logger.info(f"Found and removing existing token for: {existing_user.email}")
        AuthService.remove_token(db=db, token=existing_token)
    new_token = AuthService.add_token(
        db=db,
        token=TokenCreate(
            user_id=existing_user.id,
            payload=encoded_token,
            expires=datetime.utcnow() + timedelta(minutes=30),
        ),
    )
    if not new_token:
        logger.error(f"Failed to record token for: {existing_user.email}")
        raise HTTPException(status_code=500)
    logger.info(f"User has logged in: {existing_user.email}")
    return UserTokenResponse(access_token=encoded_token, type="bearer")


@router.get("/logout")
def logout(
    token: Annotated[UserToken, Depends(AuthUtils.get_token_from_header)],
    db: SessionLocal = Depends(get_db),
):
    existing_token = AuthService.get_token_by_user_id(db=db, user_id=token.id)
    if not existing_token:
        return
    AuthService.remove_token(db=db, token=existing_token)
    logger.info(f"User has logged out: {token.email}")
