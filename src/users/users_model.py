from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.sync_database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    books: Mapped[list["Book"]] = relationship(cascade="all, delete-orphan", lazy="joined")  # type: ignore
