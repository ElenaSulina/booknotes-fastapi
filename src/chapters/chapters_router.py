from fastapi import APIRouter, status

from src.dependencies.dependencies import (
    get_current_user_dependency,
    create_async_session_dependency,
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
async def get_chapter_by_id(
    chapter_id,
    current_user: get_current_user_dependency,
    session: create_async_session_dependency,
) -> ChaptersSchema:
    return await ChaptersService.get_chapter_by_id(session, chapter_id, current_user)


@chapters_router.post("/", status_code=status.HTTP_201_CREATED, summary="Создать главу")
async def create_chapter(
    chapter_dto: CreateChapterSchema,
    current_user: get_current_user_dependency,
    session: create_async_session_dependency,
):
    return await ChaptersService.create_chapter(session, chapter_dto, current_user)


@chapters_router.put(
    "/{chapter_id}/move", summary="Изменить порядковый номер главы (перетащить)"
)
async def move_chapter(
    chapter_id: int,
    chapter_dto: MoveChapterSchema,
    current_user: get_current_user_dependency,
    session: create_async_session_dependency,
):
    return await ChaptersService.move_chapter(session, chapter_id, chapter_dto, current_user)


@chapters_router.put("/{chapter_id}", summary="Изменить главу")
async def update_chapter(
    chapter_id,
    chapter_dto: UpdateChapterSchema,
    current_user: get_current_user_dependency,
    session: create_async_session_dependency,
) -> ChaptersSchema:
    return await ChaptersService.update_chapter(
        session, chapter_id, chapter_dto, current_user
    )


@chapters_router.delete("/{chapter_id}", summary="Удалить главу")
async def delete_chapter(
    chapter_id,
    current_user: get_current_user_dependency,
    session: create_async_session_dependency,
) -> dict:
    return await ChaptersService.delete_chapter(session, chapter_id, current_user)
