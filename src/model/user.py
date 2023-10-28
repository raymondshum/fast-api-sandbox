from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from src.model.base import Base


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    created = Column(DateTime, default=datetime.utcnow)
