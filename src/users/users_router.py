from fastapi import APIRouter

from src.dependencies.dependencies import (
    get_current_user_dependency,
    create_async_session_dependency
)
from src.users.users_schema import CreateUserSchema, UsersSchema, UsersSchemaWithBooks
from src.users.users_service import UsersService

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/me", summary="Мой профиль")
async def my_profile(
    current_user: get_current_user_dependency,
) -> UsersSchemaWithBooks:
    return current_user


@users_router.put("/me", summary="Изменить мой профиль")
async def update_my_profile(
    user_dto: CreateUserSchema,
    current_user: get_current_user_dependency,
    session: create_async_session_dependency,
) -> UsersSchema:
    return await UsersService.update_user(session, current_user.id, user_dto)


@users_router.delete("/me", summary="Удалить мой профиль")
async def delete_my_profile(
    current_user: get_current_user_dependency, session: create_async_session_dependency
) -> dict:
    return await UsersService.delete_user(session, current_user.id)
