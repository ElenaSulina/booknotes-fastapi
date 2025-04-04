from fastapi import APIRouter

from src.auth.auth_schema import Token
from src.auth.auth_service import AuthService
from src.users.users_schema import CreateUserSchema
from src.dependencies.dependencies import create_session_dependency, get_auth_form_dependency

auth_router = APIRouter(tags=["Auth"])

@auth_router.post("/login", summary="Вход через JWT токен")
def login(
    form_data: get_auth_form_dependency,
    session: create_session_dependency
) -> Token:
    return AuthService.login(
        session,
        form_data.username,
        form_data.password
    )


@auth_router.post("/signup", summary="Регистрация через JWT токен")
def signup(
    user_dto: CreateUserSchema, 
    session: create_session_dependency
    ) -> Token:
    return AuthService.signup(session, user_dto)