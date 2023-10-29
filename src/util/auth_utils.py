import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from model.schema import UserToken

logger = logging.getLogger(__name__)


class AuthUtils:
    bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
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
            AuthUtils.init_jwt_variables()
        return jwt.encode(
            raw_token,
            cls.jwt_secret_key,
            algorithm=cls.jwt_algorithm,
        )

    @classmethod
    def init_jwt_variables(cls):
        if not cls.jwt_algorithm:
            cls.jwt_algorithm = os.environ.get("JWT_ALGORITHM", None)
            logger.info(f"Initialized JWT algorithm.")
        if not cls.jwt_secret_key:
            cls.jwt_secret_key = os.environ.get("JWT_SECRET_KEY", None)
            logger.info(f"Initialized JWT secret.")
        if not cls.jwt_algorithm or not cls.jwt_secret_key:
            raise RuntimeError(f"JWT config variables not set.")
