from fastapi import APIRouter

from core.config import config
from src.auth.auth_router import auth_router
from src.books.books_router import books_router
from src.chapters.chapters_router import chapters_router
from src.notes.notes_router import notes_router
from src.users.users_router import users_router

router = APIRouter(prefix=config.API_VERSION)

router.include_router(auth_router)
router.include_router(books_router)
router.include_router(chapters_router)
router.include_router(notes_router)
router.include_router(users_router)
