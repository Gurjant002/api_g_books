from fastapi import HTTPException
from app.controller.users import query_users
from app.models.books import Book as BookModel, BookOwner as BookOwnerModel, ReadedBook as ReadedBookModel
from app.schemas.book import BookSchema, BookSchemaWithOwner, ReturnBookSchema, OwnerBookSchema
from app.config.database import Session

def get_parse_book(book: BookSchemaWithOwner) -> BookSchema:
  book_data: BookSchema = BookSchema(
      title=book.title,
      author=book.author,
      published_year=book.published_year,
      isbn=book.isbn,
      pages=book.pages,
      cover=book.cover,
      language=book.language,
      available=book.available,
      date_added=book.date_added
  )
  return book_data

def get_parse_book_owner(book: BookSchemaWithOwner, book_id: int) -> OwnerBookSchema:
  book_owner: OwnerBookSchema = OwnerBookSchema(
      book_id=book_id,
      owner_id=book.owner_id,
      date_added=book.date_added
  )
  return book_owner

def add_new_book(book: BookSchemaWithOwner = None, books: list[BookSchemaWithOwner] = None) -> BookSchemaWithOwner:
  if book:
    db = Session()

    parsed_book = get_parse_book(book)
    new_book = BookModel(**parsed_book.model_dump())
    
    parsed_owner = get_parse_book_owner(book, new_book.id)
    new_book_owner = BookOwnerModel(**parsed_owner.model_dump())
    
    db.add(new_book)
    db.add(new_book_owner)
    db.commit()
    db.refresh(new_book)
    db.refresh(new_book_owner)
    db.close()
    response = BookSchemaWithOwner.from_orm(new_book)

  if books:
    db = Session()
    book_objects: list[BookModel] = []

    for b in books:
      parsed_book = get_parse_book(b)
      new_book = BookModel(**parsed_book.model_dump())
      db.add(new_book)
      book_objects.append(new_book)
    
    db.flush()  # Flush to get the new_book.id

    for new_book, original in zip(book_objects, books):
      parsed_owner = get_parse_book_owner(original, new_book.id)
      new_book_owner = BookOwnerModel(**parsed_owner.model_dump())
      db.add(new_book_owner)


    db.commit()
    db.refresh(new_book)
    db.refresh(new_book_owner)
    db.close()
    response = "Books added successfully"
  else:
    raise ValueError("Either book or books must be provided")
  return response

def query_books(id: int = None, email: str = None) -> list[BookSchemaWithOwner] | ReturnBookSchema:
  db = Session()
  if email:
    # Assuming email is used to filter books by owner
    user = query_users(email=email, sensitive=False)
    if not user:
      db.close()
      raise HTTPException(status_code=404, detail="User not found")
    try:
      books = db.query(BookModel).join(BookOwnerModel).filter(BookOwnerModel.owner_id == user.id).all()
      response: list[ReturnBookSchema] = []
      for book in books:
          book_with_owner = ReturnBookSchema.from_orm(book)
          book_with_owner.owner_id = user.id
          response.append(book_with_owner)
      return response
    except Exception as e:
      db.close()
      raise HTTPException(status_code=500, detail=str(e))

  if id:
    book = db.query(BookModel).filter(BookModel.id == id).first()
    db.close()
    if not book:
      raise HTTPException(status_code=404, detail="Book not found")
    response = ReturnBookSchema.from_orm(book)
    return response
  
  books = db.query(BookModel).all()
  db.close()
  response = [ReturnBookSchema.from_orm(book) for book in books]
  return response