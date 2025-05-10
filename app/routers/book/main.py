from fastapi import APIRouter, HTTPException
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
