from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import DeclarativeBase, declared_attr


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
            self.password = password
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
