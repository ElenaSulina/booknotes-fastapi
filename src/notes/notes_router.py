from fastapi import APIRouter, status

from src.dependencies.dependencies import (
    get_current_user_dependency,
    create_async_session_dependency,
)
from src.notes.notes_service import NotesService
from src.notes.notes_schema import (
    CreateNoteSchema,
    MoveNoteSchema,
    NotesSchema,
    UpdateNoteSchema,
)

notes_router = APIRouter(prefix="/notes", tags=["Notes"])


@notes_router.get("/{note_id}", summary="Получить заметку по id")
async def get_note_by_id(
    note_id,
    current_user: get_current_user_dependency,
    session: create_async_session_dependency,
) -> NotesSchema:
    return await NotesService.get_note_by_id(session, note_id, current_user)


@notes_router.post("/", status_code=status.HTTP_201_CREATED, summary="Создать заметку")
async def create_note(
    note_dto: CreateNoteSchema,
    current_user: get_current_user_dependency,
    session: create_async_session_dependency,
) -> NotesSchema:
    return await NotesService.create_note(session, note_dto, current_user)


@notes_router.put(
    "/{note_id}/move", summary="Изменить порядковый номер заметки (перетащить)"
)
async def move_note(
    note_id: int,
    note_dto: MoveNoteSchema,
    current_user: get_current_user_dependency,
    session: create_async_session_dependency,
):
    return await NotesService.move_note(session, note_id, note_dto, current_user)


@notes_router.put("/{note_id}", summary="Изменить заметку")
async def update_note(
    current_user: get_current_user_dependency,
    note_id,
    note_dto: UpdateNoteSchema,
    session: create_async_session_dependency,
) -> NotesSchema:
    return await NotesService.update_note(session, note_id, note_dto, current_user)


@notes_router.delete("/{note_id}", summary="Удалить заметку")
async def delete_note(
    note_id,
    current_user: get_current_user_dependency,
    session: create_async_session_dependency,
) -> dict:

    return await NotesService.delete_note(session, note_id, current_user)
