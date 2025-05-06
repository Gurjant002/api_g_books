from app.models.books import Book as BookModel
from app.routers.schemas.book import BookSchema
from app.config.database import Session

def add_new_book(book: BookSchema) -> BookModel:
  db = Session()
  new_book = BookModel(**book.model_dump())
  db.add(new_book)
  db.commit()
  db.refresh(new_book)
  db.close()
  response = BookSchema.from_orm(new_book)
  return response