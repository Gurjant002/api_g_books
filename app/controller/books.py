from fastapi import HTTPException
from app.config.database import Session
from app.models.books import Book as BookModel, BookOwner as BookOwnerModel, ReadedBook as ReadedBookModel
from app.models.users import User
from app.schemas.book import BookSchema, ReturnBookSchema, OwnerBookSchema
from app.schemas.user import NonSensitiveUserSchema
from app.schemas.user_book import BookSchemaWithOwner
from app.controller.users import query_users

def get_parse_bookModel_bookSchemaOwner(books: BookModel, user: User) -> BookSchemaWithOwner:
  """
  Parses the BookSchemaWithOwner to ensure it has the correct structure.
  """
  if isinstance(user, User):
    user = NonSensitiveUserSchema.from_orm(user)
  return BookSchemaWithOwner(
      id=books.id,
      title=books.title,
      author=books.author,
      published_year=books.published_year,
      isbn=books.isbn,
      pages=books.pages,
      cover=books.cover,
      language=books.language,
      available=books.available,
      owner_id=user.id,
      owner=user,
      date_added=books.date_added
  )

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
    if not book:
      db.close()
      raise HTTPException(status_code=404, detail="Book not found")
    
    owner_id = db.query(BookOwnerModel).filter(BookOwnerModel.book_id == id).first()
    owner = query_users(id=owner_id.owner_id, sensitive=False)

    response = get_parse_bookModel_bookSchemaOwner(book, owner)
    return response

  books = db.query(
    BookModel,
    User
  ).select_from(BookModel).join(
    BookOwnerModel, BookModel.id == BookOwnerModel.book_id
  ).join(
    User, BookOwnerModel.owner_id == User.id
  ).all()
  db.close()
  
  response = []
  for book, user in books:
    book_with_owner = get_parse_bookModel_bookSchemaOwner(book, user)
    response.append(book_with_owner)
  
  return response