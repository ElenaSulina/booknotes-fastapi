from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.sync_database import Base


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    order: Mapped[int]
    chapter_id: Mapped[int] = mapped_column(ForeignKey("chapters.id"))
    chapter: Mapped["Chapter"] = relationship(back_populates="notes")  # type: ignore
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
