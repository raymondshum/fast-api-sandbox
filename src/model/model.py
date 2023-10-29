from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, relationship

from model.schema import UserToken
from util.auth_utils import AuthUtils


class Base(DeclarativeBase):
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


class User(Base):
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    created = Column(DateTime, default=datetime.utcnow)

    def update(self, email: str, password: str, first_name: str, last_name: str):
        if email:
            self.email = email
        if password:
            self.password = AuthUtils.hash_password(password)
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name

    def validate_jwt(self, token: UserToken) -> bool:
        return (
            token.id == self.id
            and token.email == self.email
            and token.exp.replace(tzinfo=None) > datetime.utcnow().replace(tzinfo=None)
        )


class Token(Base):
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey(User.id), unique=True, index=True)
    payload = Column(String)
    created = Column(DateTime, default=datetime.utcnow)
    expires = Column(DateTime)
    user = relationship("User", foreign_keys=["User.id"])
