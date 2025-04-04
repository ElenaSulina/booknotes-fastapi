from datetime import datetime

from pydantic import BaseModel, Field

from chapters.chapters_schema import ChaptersSchema


class CreateBookSchema(BaseModel):
    name: str = Field(max_length=1000)
    author: str = Field(max_length=1000)


class BooksSchema(CreateBookSchema):
    id: int
    user_id: int
    chapters: list[ChaptersSchema]
    created_at: datetime
