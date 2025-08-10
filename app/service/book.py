from fastapi import HTTPException
from app.config.database import get_db, db_transaction

from app.models.books import (
  Book as BookModel,
  BookOwner as BookOwnerModel,
  BorrowedBook as BorrowedBookModel
)
from app.models.users import User as UserModel

class BookService:
  def query_books(self):
    with get_db() as db:
      books = db.query(BookModel).all()
      return books
  
  def query_books_with_owner(self) -> list:
    """
    Queries the database to retrieve a list of books along with their respective owners.

    Returns:
      list: A list of tuples, where each tuple contains a BookModel instance and the corresponding UserModel instance representing the owner.
    """
    with get_db() as db:
      books = db.query(
        BookModel,
        UserModel
      ).select_from(BookModel).join(
        BookOwnerModel, BookModel.id == BookOwnerModel.book_id
      ).join(
        UserModel, BookOwnerModel.owner_id == UserModel.id
      ).all()
      return books
  
  def query_book_by_id(book_id: int) -> BookModel:
    with get_db() as db:
      book = db.query(BookModel).filter(BookModel.id == book_id).first()
      if not book:
        raise HTTPException(status_code=404, detail="Book not found")
      return book

  def query_book_by_owner_id(owner_id: int) -> list:
    with get_db() as db:
      books = db.query(BookModel).join(BookOwnerModel).filter(BookOwnerModel.owner_id == owner_id).all()
      return books