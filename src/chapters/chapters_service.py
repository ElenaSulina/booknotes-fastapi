from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from dependencies.dependencies import create_session_dependency
from chapters.chapters_schema import CreateChapterSchema, UpdateChapterSchema
from src.chapters.chapters_model import Chapter
from users.users_schema import UsersSchema
from books.books_service import BooksService


class ChaptersService:

    @classmethod
    def create_chapter(
        cls, session: Session, chapter_dto: CreateChapterSchema, current_user
    ):
        chapter = Chapter()

        book = BooksService.get_book_by_id(session, chapter_dto.book_id, current_user)

        for key, value in chapter_dto.model_dump().items():
            setattr(chapter, key, value) if value else None

        count = session.query(Chapter).filter_by(book_id=chapter.book_id).count()
        chapter.order = count + 1

        session.add(chapter)
        session.commit()
        session.refresh(chapter)
        return chapter

    @classmethod
    def delete_chapter(cls, session: Session, chapter_id, current_user):
        chapter = cls.get_chapter_by_id(session, chapter_id, current_user)

        session.delete(chapter)
        session.commit()

        return {"status": "ok", "message": "Chapter has been deleted successfully"}

    @classmethod
    def get_chapter_by_id(
        cls, session: Session, chapter_id, current_user: UsersSchema
    ):
        chapter = session.get(Chapter, chapter_id)

        if not chapter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found"
            )

        book = BooksService.get_book_by_id(session, chapter.book_id, current_user)

        return chapter

    @classmethod
    def get_chapters_in_book(cls, session: Session, chapter: Chapter):
        query = session.query(Chapter).filter_by(book_id=chapter.book_id)
        chapters_in_book: list[Chapter] = session.execute(query).scalars().all()
        return chapters_in_book

    @classmethod
    def move_chapter(
        cls, session: Session, chapter_id, chapter_dto: Chapter, current_user
    ):
        chapter: Chapter = cls.get_chapter_by_id(session, chapter_id, current_user)

        current_order = chapter.order
        new_order = chapter_dto.order

        chapters = cls.get_chapters_in_book(session, chapter)
        chapters_count = len(chapters)

        # order не может быть больше, чем кол-во глав
        if new_order > chapters_count:
            new_order = chapters_count

        # если нужно уменьшить порядковый номер
        if current_order > new_order:
            for item in chapters:
                if item.order >= new_order and item.order < current_order:
                    item.order += 1

        # если нужно увеличить порядковый номер
        elif current_order < new_order:
            for item in chapters:
                if item.order <= new_order and item.order > current_order:
                    item.order -= 1

        chapter.order = new_order

        session.commit()

        session.refresh(chapter)
        return chapter

    @classmethod
    def update_chapter(
        cls,
        session: Session,
        chapter_id,
        chapter_dto: UpdateChapterSchema,
        current_user: UsersSchema,
    ):

        chapter = cls.get_chapter_by_id(session, chapter_id, current_user)

        for key, value in chapter_dto.model_dump().items():
            setattr(chapter, key, value) if value else None

        session.commit()
        session.refresh(chapter)

        return chapter
