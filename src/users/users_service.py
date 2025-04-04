from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound


from src.users.users_model import User
from src.users.users_schema import CreateUserSchema


class UsersService:

    @classmethod
    def create_user(cls, session: Session, user_dto: CreateUserSchema):

        cls.raise_http_exception_if_user_already_exists(session, user_dto)

        user_dto.password = cls.hash_password(user_dto.password)

        user = User()
        for key, value in user_dto.model_dump().items():
            setattr(user, key, value) if value else None

        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @classmethod
    def delete_user(cls, session: Session, user_id):
        user = cls.get_user_by_id(session, user_id)
        session.delete(user)
        session.commit()

        return {"status": "ok", "message": "User has been deleted successfully"}

    @classmethod
    def get_user_by_id(cls, session: Session, id):

        try:
            user = session.get_one(User, id)
        except NoResultFound:
            raise HTTPException(404, "User not found")
        else:
            return user

    @classmethod
    def get_user_by_email(cls, session: Session, email):
        user = session.execute(select(User).where(User.email == email)).scalar()

        if not user:
            return False

        return user

    @classmethod
    def hash_password(cls, password: str) -> str:
        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return password_context.hash(password)

    @classmethod
    def raise_http_exception_if_user_already_exists(cls, session, user_dto):
        user_exists = cls.get_user_by_email(session, user_dto.email)

        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this Email already exists",
            )

    @classmethod
    def update_user(
        cls, session: Session, current_user_id, user_dto: CreateUserSchema
    ):
        user_dto.password = cls.hash_password(user_dto.password)

        user = cls.get_user_by_id(session, current_user_id)
        for key, value in user_dto.model_dump().items():
            setattr(user, key, value) if value else None

        session.commit()
        session.refresh(user)

        return user
