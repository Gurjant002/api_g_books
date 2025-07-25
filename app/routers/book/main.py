import os
from fastapi import APIRouter, HTTPException, UploadFile, Depends
import shutil
from app.schemas.book import BookSchemaWithOwner, ReturnBookSchema
from app.controller.books import add_new_book, query_books
from app.controller.users import oauth2_scheme

router = APIRouter()

@router.post("/add-book", tags=["Books"], response_model=BookSchemaWithOwner, description="Add a new book")
async def new_book(book: BookSchemaWithOwner):
  if not book:
    raise HTTPException(status_code=400, detail="Book data is required")
  response = add_new_book(book)
  return response

@router.post("/add-books", tags=["Books"], response_model=BookSchemaWithOwner | str, description="Add a new book")
async def new_books(books: list[BookSchemaWithOwner]):
  try:
    if books is None or len(books) == 0:
      raise HTTPException(status_code=400, detail="Book data is required")
    response = add_new_book(books=books)
    return response if isinstance(response, BookSchemaWithOwner) else "Books added successfully"
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-all-books", tags=["Books"], response_model=list[ReturnBookSchema], description="Get all books")
async def get_all_books():
  try:
    response = query_books()
    return response
  except Exception as e:
    print(f"Error fetching books: {e}")
    raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-book/{book_id}", tags=["Books"], response_model=ReturnBookSchema, description="Get a book by ID")
async def get_book(book_id: int):
  response = query_books(id=book_id)
  if not response:
    raise HTTPException(status_code=404, detail="Book not found")
  return response

@router.get("/owned-books", tags=["Books"], description="Get book owned by the user")
async def get_owned_books(token: str = Depends(oauth2_scheme)):
  response = query_books(token=token)
  return response

@router.post("/upload-cover", tags=["Books"], description="Upload a book cover")
async def upload_cover(file: UploadFile, description: str = None):
  # Here you would typically save the file to a directory or cloud storage
  # For demonstration, we'll just return the filename and content type
  os.makedirs("static", exist_ok=True)
  file_path = f"static/{file.filename}"
  with open(file_path, "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)
    
  return {
    "filename": file.filename,
    "content_type": file.content_type
  }

@router.get("/book-cover/{book_id}", tags=["Books"], description="Get book cover")
async def get_book_cover(book_id: str):
  # This function would typically query the database for the book cover path
  # For demonstration, we'll just return a static path
  return f"static/book_covers/{book_id}.jpg"


