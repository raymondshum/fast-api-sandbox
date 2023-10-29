import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from model.schema import UserToken

logger = logging.getLogger(__name__)


class AuthUtils:
    bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
    security = HTTPBearer()
    jwt_secret_key: str = None
    jwt_algorithm: str = None

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.bcrypt.hash(password)

    @classmethod
    def authenticate_user(cls, password: str, hashed_password: str) -> bool:
        return cls.bcrypt.verify(password, hashed_password)

    @classmethod
    def get_jwt(cls, email: EmailStr, id: str, expires_in: timedelta):
        token_expiration = datetime.utcnow() + expires_in
        raw_token: Dict[str, Any] = UserToken(
            id=id, email=email, exp=token_expiration
        ).model_dump()
        if not cls.jwt_secret_key or not cls.jwt_algorithm:
            AuthUtils._init_jwt_variables()
        return jwt.encode(
            raw_token,
            cls.jwt_secret_key,
            algorithm=cls.jwt_algorithm,
        )

    @classmethod
    def get_token_from_header(
        cls, credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> UserToken:
        token = credentials.credentials
        try:
            payload = jwt.decode(
                token=token, algorithms=[cls.jwt_algorithm], key=cls.jwt_secret_key
            )
            if not payload:
                raise HTTPException(status_code=401, detail="JWT validation failed.")
            return UserToken(**payload)
        except JWTError as e:
            raise HTTPException(status_code=401, detail="JWT validation failed.")

    @classmethod
    def _init_jwt_variables(cls):
        if not cls.jwt_algorithm:
            cls.jwt_algorithm = os.environ.get("JWT_ALGORITHM", None)
            logger.info(f"Initialized JWT algorithm.")
        if not cls.jwt_secret_key:
            cls.jwt_secret_key = os.environ.get("JWT_SECRET_KEY", None)
            logger.info(f"Initialized JWT secret.")
        if not cls.jwt_algorithm or not cls.jwt_secret_key:
            raise RuntimeError(f"JWT config variables not set.")
