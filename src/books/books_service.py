from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from books.books_schema import BooksSchema, CreateBookSchema
from src.books.books_model import Book
from users.users_schema import UsersSchema


class BooksService:
    @classmethod
    def create_book(
        cls, session: Session, book_dto: CreateBookSchema, current_user: UsersSchema
    ):
        book = Book()

        for key, value in book_dto.model_dump().items():
            setattr(book, key, value) if value else None

        book.user_id = current_user.id

        session.add(book)
        session.commit()
        session.refresh(book)
        return book

    @classmethod
    def delete_book(cls, session: Session, book_id, current_user):
        book = cls.get_book_by_id(session, book_id, current_user)

        session.delete(book)
        session.commit()

        return {"status": "ok", "message": "Book has been deleted successfully "}

    @classmethod
    def get_book_by_id(
        cls, session: Session, book_id: int, current_user: UsersSchema
    ) -> BooksSchema:
        try:
            book = session.get_one(Book, book_id)
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
    def update_book(
        cls,
        session: Session,
        book_id,
        book_dto: CreateBookSchema,
        current_user: UsersSchema,
    ):
        book = cls.get_book_by_id(session, book_id, current_user)

        for key, value in book_dto.model_dump().items():
            setattr(book, key, value) if value else None

        session.commit()
        session.refresh(book)

        return book
