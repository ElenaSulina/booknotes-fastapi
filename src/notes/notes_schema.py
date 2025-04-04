from pydantic import BaseModel, Field


class UpdateNoteSchema(BaseModel):
    text: str = Field(max_length=10000)


class CreateNoteSchema(UpdateNoteSchema):
    chapter_id: int


class NotesSchema(CreateNoteSchema):
    id: int
    order: int = Field(gt=0)


class MoveNoteSchema(BaseModel):
    order: int = Field(gt=0)
