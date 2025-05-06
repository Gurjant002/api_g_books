from app.config.database import Base
from sqlalchemy import Column, Integer, String

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=255), unique=False, nullable=False) # Activate unique=True for title
    author = Column(String, nullable=False)
    published_year = Column(Integer, nullable=True)
    isbn = Column(String, unique=False, nullable=True) # Activate unique=True for isbn
    pages = Column(Integer, nullable=True)
    cover = Column(String, nullable=True)
    language = Column(String, nullable=True)

