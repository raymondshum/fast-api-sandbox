import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from model.model import Token
from model.schema import TokenCreate, UserToken


class AuthService:
    @staticmethod
    def add_token(db: Session, token: TokenCreate) -> Token:
        new_token = Token(
            id=str(uuid.uuid1()),
            user_id=token.user_id,
            payload=token.payload,
            created=datetime.utcnow(),
            expires=token.expires,
        )
        db.add(new_token)
        db.commit()
        db.refresh(new_token)
        return new_token

    @staticmethod
    def remove_token(db: Session, token: Token):
        db.delete(token)
        db.commit()

    @staticmethod
    def token_is_active(db: Session, token: UserToken):
        if not token:
            return False
        existing_token = AuthService.get_token_by_user_id(db=db, user_id=token.id)
        if not existing_token:
            return False
        return datetime.utcnow().replace(tzinfo=None) < existing_token.expires.replace(
            tzinfo=None
        )

    @staticmethod
    def get_token_by_user_id(db: Session, user_id: str):
        return db.query(Token).filter(Token.user_id == user_id).first()

    @staticmethod
    def get_token_by_payload(db: Session, payload: str):
        return db.query(Token).filter(Token.payload == payload).first()
