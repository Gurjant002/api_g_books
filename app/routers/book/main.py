from fastapi import APIRouter
from app.routers.schemas.book import BookSchema
from app.controller.books import add_new_book

router = APIRouter()

@router.post("/add-book", tags=["Books"], response_model=BookSchema, description="Add a new book")
async def new_book(book: BookSchema):
  response = add_new_book(book)
  return response
