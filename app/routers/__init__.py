from fastapi import APIRouter

from app.routers.search import router as search_router
from app.routers.books import router as books_router
from app.routers.request import router as request_router
from app.routers.auth import router as auth_router
from app.routers.oauth import router as oauth_router

router = APIRouter(tags=["api/v1"], prefix="/api/v1")
router.include_router(search_router, tags=["search"], prefix="/search")
router.include_router(request_router, tags=["request"], prefix="/request")
router.include_router(books_router, tags=["books"], prefix="/books")
# router.include_router(auth_router, tags=["auth"], prefix="/auth")
# router.include_router(oauth_router, tags=["oauth"], prefix="/oauth")
