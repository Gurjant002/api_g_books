from app.config.database import Base
from sqlalchemy import Column, Integer, String
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=255), unique=True, nullable=False)
    email = Column(String(length=255), unique=True, nullable=False)
    password = Column(String(length=255), nullable=False)
    first_name = Column(String(length=255), nullable=False)
    last_name = Column(String(length=255), nullable=False)
    is_active = Column(Integer, default=1)
    is_superuser = Column(Integer, default=0)
    is_verified = Column(Integer, default=0)
    date_joined = Column(String(length=255), nullable=False, default=datetime.utcnow().isoformat()+ 'Z')
    