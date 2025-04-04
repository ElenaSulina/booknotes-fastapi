from pydantic import BaseModel, Field

from src.notes.notes_schema import NotesSchema


class UpdateChapterSchema(BaseModel):
    name: str = Field(max_length=1000)


class CreateChapterSchema(UpdateChapterSchema):
    book_id: int


class ChaptersSchema(CreateChapterSchema):
    id: int
    order: int = Field(gt=0)
    notes: list[NotesSchema]


class MoveChapterSchema(BaseModel):
    order: int = Field(gt=0)
