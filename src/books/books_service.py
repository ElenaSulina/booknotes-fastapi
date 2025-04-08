from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from books.books_schema import BooksSchema, CreateBookSchema
from src.books.books_model import Book
from users.users_schema import UsersSchema


class BooksService:

    @classmethod
    async def create_book(
        cls, session: AsyncSession, book_dto: CreateBookSchema, current_user: UsersSchema
    ):
        book = Book()

        for key, value in book_dto.model_dump().items():
            setattr(book, key, value) if value else None

        book.user_id = current_user.id

        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    @classmethod
    async def delete_book(cls, session: AsyncSession, book_id, current_user):
        book = await cls.get_book_by_id(session, book_id, current_user)

        await session.delete(book)
        await session.commit()

        return {"status": "ok", "message": "Book has been deleted successfully "}


    @classmethod
    async def get_book_by_id(
        cls, session: AsyncSession, book_id: int, current_user: UsersSchema
    ) -> BooksSchema:
        try:
            book = await session.get_one(Book, int(book_id))
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )
        else:
            if not (book.user_id == current_user.id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to access",
                )
            else:
                return book

    @classmethod
    async def update_book(
        cls,
        session: AsyncSession,
        book_id,
        book_dto: CreateBookSchema,
        current_user: UsersSchema,
    ):
        book = await cls.get_book_by_id(session, book_id, current_user)

        for key, value in book_dto.model_dump().items():
            setattr(book, key, value) if value else None

        await session.commit()
        await session.refresh(book)

        return book
