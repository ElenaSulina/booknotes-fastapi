from pydantic import BaseModel, EmailStr, Field

from src.books.books_schema import BooksSchema


class CreateUserSchema(BaseModel):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    # email: EmailStr
    email: str
    password: str


class UsersSchema(CreateUserSchema):
    id: int


class UsersSchemaWithBooks(UsersSchema):
    books: list[BooksSchema]
