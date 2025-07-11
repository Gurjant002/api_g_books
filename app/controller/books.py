from app.models.books import Book as BookModel
from app.schemas.book import BookSchema, ReturnBookSchema
from app.config.database import Session

def add_new_book(book: BookSchema = None, books: list[BookSchema] = None) -> BookSchema:
  if book:
    db = Session()
    new_book = BookModel(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    db.close()
    response = BookSchema.from_orm(new_book)
  if books:
    db = Session()
    for b in books:
      new_book = BookModel(**b.model_dump())
      db.add(new_book)
    db.commit()
    db.refresh(new_book)
    db.close()
    response = "Books added successfully"
  else:
    raise ValueError("Either book or books must be provided")
  return response

def query_books(id: int = None) -> list[BookSchema] | ReturnBookSchema:
  db = Session()
  if id:
    book = db.query(BookModel).filter(BookModel.id == id).first()
    db.close()
    if not book:
      return None
    response = ReturnBookSchema.from_orm(book)
    return response
  
  books = db.query(BookModel).all()
  db.close()
  response = [ReturnBookSchema.from_orm(book) for book in books]
  return response