from app.config.database import Base
from sqlalchemy import Column, Integer, String, Boolean

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
    description = Column(String, nullable=True)
    available = Column(Boolean, default=True)  # Default to 1 for availability

class RentedBook(Base):
    __tablename__ = 'rented_books'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, nullable=False)
    owner_id = Column(Integer, nullable=False)  # Assuming owner_id is an integer
    date_added = Column(String, nullable=True)  # Assuming date_added is a string in ISO format

class ReadedBook(Base):
    __tablename__ = 'readed_books'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)  # Assuming user_id is an integer
    start = Column(String, nullable=True)  # Assuming start is a string in ISO format
    end = Column(String, nullable=True)  # Assuming end is a string in ISO format
