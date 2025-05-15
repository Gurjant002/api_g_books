from fastapi import APIRouter

from app.routers.book.main import router as book_router
from app.routers.user.main import router as user_router

router = APIRouter()
router.include_router(book_router, prefix="/api/books", tags=["Books"])
router.include_router(user_router, prefix="/api/users", tags=["Users"])
