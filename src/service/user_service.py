import logging
import uuid

from pydantic import EmailStr
from sqlalchemy import UUID
from sqlalchemy.orm import Session

from model.model import User
from model.schema import UserSchema, UserUpdate

logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    def create_user(db: Session, user: UserSchema) -> User:
        new_user = User(**user.model_dump())
        new_user.id = str(uuid.uuid1())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: EmailStr) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def delete_user(db: Session, user: User) -> None:
        db.delete(user)
        db.commit()

    @staticmethod
    def update_user(
        db: Session, updated_fields: UserUpdate, existing_user: User
    ) -> User:
        existing_user.update(**updated_fields.model_dump())
        db.commit()
        db.refresh(existing_user)
        return existing_user
