import os
from fastapi import APIRouter, HTTPException, UploadFile
import shutil
from app.schemas.book import BookSchema, ReturnBookSchema
from app.controller.books import add_new_book, query_books

router = APIRouter()

@router.post("/add-book", tags=["Books"], response_model=BookSchema, description="Add a new book")
async def new_book(book: BookSchema):
  response = add_new_book(book)
  return response

@router.get("/get-all-books", tags=["Books"], response_model=list[ReturnBookSchema], description="Get all books")
async def get_all_books():
  response = query_books()
  return response

@router.get("/get-book/{book_id}", tags=["Books"], response_model=ReturnBookSchema, description="Get a book by ID")
async def get_book(book_id: int):
  response = query_books(id=book_id)
  if not response:
    raise HTTPException(status_code=404, detail="Book not found")
  return response

@router.get("/hello")
async def hello():
  return {"message": "Hello World"}

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
