from fastapi import APIRouter

from src.auth.auth_schema import Token
from src.auth.auth_service import AuthService
from src.users.users_schema import CreateUserSchema
from src.dependencies.dependencies import get_auth_form_dependency, create_async_session_dependency

auth_router = APIRouter(tags=["Auth"])

@auth_router.post("/login", summary="Вход через JWT токен")
async def login(
    form_data: get_auth_form_dependency,
    session: create_async_session_dependency
) -> Token:
    return await AuthService.login(
        session,
        form_data.username,
        form_data.password
    )


@auth_router.post("/signup", summary="Регистрация через JWT токен")
async def signup(
    user_dto: CreateUserSchema, 
    session: create_async_session_dependency
    ) -> Token:
    return await AuthService.signup(session, user_dto)