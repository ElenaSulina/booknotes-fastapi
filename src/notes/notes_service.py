from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.chapters.chapters_service import ChaptersService
from notes.notes_schema import CreateNoteSchema, UpdateNoteSchema
from src.notes.notes_model import Note


class NotesService:

    @classmethod
    async def create_note(cls, session: AsyncSession, note_dto: CreateNoteSchema, current_user):
        note = Note()

        chapter = await ChaptersService.get_chapter_by_id(
            session, note_dto.chapter_id, current_user
        )

        for key, value in note_dto.model_dump().items():
            setattr(note, key, value) if value else None

        query = select(func.count()).select_from(Note).filter_by(chapter_id=note.chapter_id)
        result = await session.execute(query)
        count = result.scalar()

        note.order = count + 1

        session.add(note)
        await session.commit()
        await session.refresh(note)
        return note
    

    # Нужно менять order остальных заметок!!!!
    @classmethod
    async def delete_note(cls, session: AsyncSession, note_id, current_user):
        note = await cls.get_note_by_id(session, note_id, current_user)

        await session.delete(note)
        await session.commit()

        return {"status": "ok", "message": "Note has been deleted successfully "}


    @classmethod
    async def get_note_by_id(cls, session: AsyncSession, note_id, current_user):
        note = await session.get(Note, int(note_id))

        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
            )

        chapter = await ChaptersService.get_chapter_by_id(
            session, note.chapter_id, current_user
        )

        return note
    

    @classmethod
    async def get_notes_in_chapter(cls, session: AsyncSession, note: Note):
        query = select(Note).filter_by(chapter_id=note.chapter_id)
        result = await session.execute(query)
        notes_in_chapter: list[Note] = result.scalars().unique().all()
        return notes_in_chapter
    

    @classmethod
    async def update_note(
        cls, session: AsyncSession, note_id, note_dto: UpdateNoteSchema, current_user
    ):
        note: Note = await cls.get_note_by_id(session, note_id, current_user)
        note.text = note_dto.text

        await session.commit()
        await session.refresh(note)

        return note


    @classmethod
    async def move_note(cls, session: AsyncSession, note_id, note_dto, current_user):
        note: Note = await cls.get_note_by_id(session, note_id, current_user)

        current_order = note.order
        new_order = note_dto.order

        notes = await cls.get_notes_in_chapter(session, note)
        notes_count = len(notes)

        # order не может быть больше, чем кол-во глав
        if new_order > notes_count:
            new_order = notes_count

        # если нужно уменьшить порядковый номер
        if current_order > new_order:
            for item in notes:
                if item.order >= new_order and item.order < current_order:
                    item.order += 1

        # если нужно увеличить порядковый номер
        elif current_order < new_order:
            for item in notes:
                if item.order <= new_order and item.order > current_order:
                    item.order -= 1

        note.order = new_order

        await session.commit()

        await session.refresh(note)
        return note