from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

import jwt

from core.config import config
from core.database import create_session
from src.users.users_model import User
from src.auth.auth_schema import Token
from src.users.users_service import UsersService
from src.users.users_schema import CreateUserSchema


class AuthService:

    @classmethod
    def authenticate_user(cls, session: Session, username, password):
        query = select(User).where(User.email == username)
        result = session.execute(query)
        user = result.scalar()

        if not user:
            return False

        if not cls.verify_password(password, user.password):
            return False

        return user

    @classmethod
    def create_access_token(cls, user: User):

        payload = dict(
            sub=user.email,
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            created_at=str(user.created_at),
        )

        # issued_at = datetime.now()
        expire = datetime.now() + timedelta(hours=24)
        payload.update(dict(exp=expire))  # iat=issued_at,
        encoded_jwt = jwt.encode(
            payload,
            config.JWT_SECRET_KEY.get_secret_value(),
            algorithm=config.JWT_ALGORITHM,
        )

        return Token(access_token=encoded_jwt, token_type="bearer")

    @classmethod
    def get_current_user(
        cls,
        token: Annotated[str, Depends(config.oauth2_scheme)],
        session: Session = Depends(create_session),
    ):
        payload = jwt.decode(
            token,
            config.JWT_SECRET_KEY.get_secret_value(),
            algorithms=[config.JWT_ALGORITHM],
        )
        username = payload.get("sub")

        return UsersService.get_user_by_email(session, email=username)

    @classmethod
    def login(cls, session: Session, username, password) -> Token:
        user = cls.authenticate_user(session, username, password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return cls.create_access_token(user)

    @classmethod
    def signup(cls, session: Session, user_dto: CreateUserSchema) -> Token:
        user = UsersService.create_user(session, user_dto)
        return cls.create_access_token(user)

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return password_context.verify(plain_password, hashed_password)
