from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound


from src.users.users_model import User
from src.users.users_schema import CreateUserSchema


class UsersService:

    @classmethod
    async def create_user(cls, session: AsyncSession, user_dto: CreateUserSchema):

        await cls.raise_http_exception_if_user_already_exists(session, user_dto)

        user_dto.password = cls.hash_password(user_dto.password)

        user = User()
        for key, value in user_dto.model_dump().items():
            setattr(user, key, value) if value else None

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @classmethod
    async def delete_user(cls, session: AsyncSession, user_id):
        user = await cls.get_user_by_id(session, user_id)
        await session.delete(user)
        await session.commit()

        return {"status": "ok", "message": "User has been deleted successfully"}

    @classmethod
    async def get_user_by_id(cls, session: AsyncSession, id):

        try:
            user = await session.get_one(User, id)
        except NoResultFound:
            raise HTTPException(404, "User not found")
        else:
            return user

    @classmethod
    async def get_user_by_email(cls, session: AsyncSession, email):
        user = await session.execute(select(User).where(User.email == email))
        user = user.scalar()

        if not user:
            return False

        return user

    @classmethod
    def hash_password(cls, password: str) -> str:
        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return password_context.hash(password)

    @classmethod
    async def raise_http_exception_if_user_already_exists(cls, session, user_dto):
        user_exists = await cls.get_user_by_email(session, user_dto.email)

        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this Email already exists",
            )

    @classmethod
    async def update_user(
        cls, session: AsyncSession, current_user_id, user_dto: CreateUserSchema
    ):
        user_dto.password = cls.hash_password(user_dto.password)

        user = await cls.get_user_by_id(session, current_user_id)

        for key, value in user_dto.model_dump().items():
            setattr(user, key, value) if value else None

        await session.commit()
        await session.refresh(user)

        return user
