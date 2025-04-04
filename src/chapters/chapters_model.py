from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from core.database import Base


class Chapter(Base):
    __tablename__ = "chapters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    order: Mapped[int]
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    book: Mapped["Book"] = relationship(back_populates="chapters")  # type: ignore
    notes: Mapped[list["Note"]] = relationship(back_populates="chapter", cascade="all, delete-orphan", lazy="joined")  # type: ignore
