from fastapi import APIRouter

from app.api.routes.search import router as search_router
from app.api.routes.books import router as books_router

router = APIRouter(tags=["api", "v1"], prefix="/api/v1")
router.include_router(search_router, tags=["search"], prefix="/search")
router.include_router(books_router, tags=["books"], prefix="/books")
