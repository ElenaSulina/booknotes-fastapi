from fastapi import APIRouter, status

from src.dependencies.dependencies import (
    get_current_user_dependency,
    create_session_dependency,
)
from src.chapters.chapters_service import ChaptersService
from src.chapters.chapters_schema import (
    ChaptersSchema,
    CreateChapterSchema,
    MoveChapterSchema,
    UpdateChapterSchema,
)


chapters_router = APIRouter(prefix="/chapters", tags=["Chapters"])


@chapters_router.get("/{chapter_id}", summary="Получить главу по id")
def get_chapter_by_id(
    chapter_id,
    current_user: get_current_user_dependency,
    session: create_session_dependency,
) -> ChaptersSchema:
    return ChaptersService.get_chapter_by_id(session, chapter_id, current_user)


@chapters_router.post("/", status_code=status.HTTP_201_CREATED, summary="Создать главу")
def create_chapter(
    chapter_dto: CreateChapterSchema,
    current_user: get_current_user_dependency,
    session: create_session_dependency,
) -> ChaptersSchema:
    return ChaptersService.create_chapter(session, chapter_dto, current_user)


@chapters_router.put(
    "/{chapter_id}/move", summary="Изменить порядковый номер главы (перетащить)"
)
def move_chapter(
    chapter_id: int,
    chapter_dto: MoveChapterSchema,
    current_user: get_current_user_dependency,
    session: create_session_dependency,
):
    return ChaptersService.move_chapter(session, chapter_id, chapter_dto, current_user)


@chapters_router.put("/{chapter_id}", summary="Изменить главу")
def update_chapter(
    chapter_id,
    chapter_dto: UpdateChapterSchema,
    current_user: get_current_user_dependency,
    session: create_session_dependency,
) -> ChaptersSchema:
    return ChaptersService.update_chapter(
        session, chapter_id, chapter_dto, current_user
    )


@chapters_router.delete("/{chapter_id}", summary="Удалить главу")
def delete_chapter(
    chapter_id,
    current_user: get_current_user_dependency,
    session: create_session_dependency,
) -> dict:
    return ChaptersService.delete_chapter(session, chapter_id, current_user)
