from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from src.chapters.chapters_service import ChaptersService
from notes.notes_schema import CreateNoteSchema, UpdateNoteSchema
from src.notes.notes_model import Note


class NotesService:

    @classmethod
    def create_note(cls, session: Session, note_dto: CreateNoteSchema, current_user):
        note = Note()

        chapter = ChaptersService.get_chapter_by_id(
            session, note_dto.chapter_id, current_user
        )

        for key, value in note_dto.model_dump().items():
            setattr(note, key, value) if value else None

        count = session.query(Note).filter_by(chapter_id=note.chapter_id).count()
        note.order = count + 1

        session.add(note)
        session.commit()
        session.refresh(note)
        return note

    @classmethod
    def get_note_by_id(cls, session: Session, note_id, current_user):
        note = session.get(Note, note_id)

        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
            )

        chapter = ChaptersService.get_chapter_by_id(
            session, note.chapter_id, current_user
        )

        return note

    @classmethod
    def update_note(
        cls, session: Session, note_id, note_dto: UpdateNoteSchema, current_user
    ):
        note: Note = cls.get_note_by_id(session, note_id, current_user)
        note.text = note_dto.text

        session.commit()
        session.refresh(note)

        return note

    @classmethod
    def move_note(cls, session: Session, note_id, note_dto, current_user):
        note: Note = cls.get_note_by_id(session, note_id, current_user)

        current_order = note.order
        new_order = note_dto.order

        query = session.query(Note).filter_by(chapter_id=note.chapter_id)
        notes_in_chapter: list[Note] = session.execute(query).scalars().all()
        count_notes_in_chapter = len(notes_in_chapter)

        # order не может быть больше, чем кол-во глав
        if new_order > count_notes_in_chapter:
            new_order = count_notes_in_chapter

        # если нужно уменьшить порядковый номер
        if current_order > new_order:
            for item in notes_in_chapter:
                if item.order >= new_order and item.order < current_order:
                    item.order += 1

        # если нужно увеличить порядковый номер
        elif current_order < new_order:
            for item in notes_in_chapter:
                if item.order <= new_order and item.order > current_order:
                    item.order -= 1

        note.order = new_order

        session.commit()

        session.refresh(note)
        return note

    @classmethod
    def delete_note(cls, session: Session, note_id, current_user):
        note = cls.get_note_by_id(session, note_id, current_user)

        session.delete(note)
        session.commit()

        return {"status": "ok", "message": "Note has been deleted successfully "}
