from fastapi import APIRouter, status

from src.dependencies.dependencies import (
    get_current_user_dependency,
    create_async_session_dependency
)
from src.books.books_service import BooksService
from src.books.books_schema import BooksSchema, CreateBookSchema

books_router = APIRouter(prefix="/books", tags=["Books"])


@books_router.get("/{book_id}", summary="Получить книгу по id")
async def get_book_by_id(
    book_id: int,
    current_user: get_current_user_dependency,
    session: create_async_session_dependency,
) -> BooksSchema:
    return await BooksService.get_book_by_id(session, book_id, current_user)


@books_router.post("/", status_code=status.HTTP_201_CREATED, summary="Создать книгу")
async def create_book(
    book_dto: CreateBookSchema,
    current_user: get_current_user_dependency,
    session: create_async_session_dependency,
) -> BooksSchema:
    return await BooksService.create_book(session, book_dto, current_user)


@books_router.put("/{book_id}", summary="Изменить книгу")
async def update_book(
    book_id,
    book_dto: CreateBookSchema,
    current_user: get_current_user_dependency,
    session: create_async_session_dependency,
) -> BooksSchema:
    return await BooksService.update_book(session, book_id, book_dto, current_user)


@books_router.delete("/{book_id}", summary="Удалить книгу")
async def delete_book(
    book_id,
    current_user: get_current_user_dependency,
    session: create_async_session_dependency,
) -> dict:
    return await BooksService.delete_book(session, book_id, current_user)
