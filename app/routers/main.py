from fastapi import APIRouter

from app.routers.book.main import router as book_router

router = APIRouter()
router.include_router(book_router, prefix="/books", tags=["Books"])
