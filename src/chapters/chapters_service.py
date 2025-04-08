from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from chapters.chapters_schema import CreateChapterSchema, UpdateChapterSchema
from src.chapters.chapters_model import Chapter
from users.users_schema import UsersSchema
from books.books_service import BooksService


class ChaptersService:

    @classmethod
    async def create_chapter(
        cls, session: AsyncSession, chapter_dto: CreateChapterSchema, current_user
    ):
        chapter = Chapter()

        book = await BooksService.get_book_by_id(session, chapter_dto.book_id, current_user)

        for key, value in chapter_dto.model_dump().items():
            setattr(chapter, key, value) if value else None

        query = select(func.count()).select_from(Chapter).filter_by(book_id=chapter.book_id)
        result = await session.execute(query)
        count = result.scalar()
      
        chapter.order = count + 1

        session.add(chapter)
        await session.commit()
        await session.refresh(chapter)
        return chapter
    

    # Нужно менять order остальных глав!!!!
    @classmethod
    async def delete_chapter(cls, session: AsyncSession, chapter_id, current_user):
        chapter = await cls.get_chapter_by_id(session, chapter_id, current_user)

        await session.delete(chapter)
        await session.commit()

        return {"status": "ok", "message": "Chapter has been deleted successfully"}


    @classmethod
    async def get_chapter_by_id(
        cls, session: AsyncSession, chapter_id, current_user: UsersSchema
    ):
        chapter = await session.get(Chapter, int(chapter_id))

        if not chapter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found"
            )

        book = await BooksService.get_book_by_id(session, chapter.book_id, current_user)

        return chapter


    @classmethod
    async def get_chapters_in_book(cls, session: AsyncSession, chapter: Chapter):
        query = select(Chapter).filter_by(book_id=chapter.book_id)
        result = await session.execute(query)
        chapters_in_book: list[Chapter] = result.scalars().unique().all()
        return chapters_in_book


    @classmethod
    async def move_chapter(
        cls, session: AsyncSession, chapter_id, chapter_dto: Chapter, current_user
    ):
        chapter: Chapter = await cls.get_chapter_by_id(session, chapter_id, current_user)

        current_order = chapter.order
        new_order = chapter_dto.order

        chapters = await cls.get_chapters_in_book(session, chapter)
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

        await session.commit()

        await session.refresh(chapter)
        return chapter


    @classmethod
    async def update_chapter(
        cls,
        session: AsyncSession,
        chapter_id,
        chapter_dto: UpdateChapterSchema,
        current_user: UsersSchema,
    ):

        chapter = await cls.get_chapter_by_id(session, chapter_id, current_user)

        for key, value in chapter_dto.model_dump().items():
            setattr(chapter, key, value) if value else None

        await session.commit()
        await session.refresh(chapter)

        return chapter
