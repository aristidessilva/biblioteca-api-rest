from pydantic import BaseModel, ConfigDict, Field

from app.schemas.author import AuthorRead


class BookBase(BaseModel):
    title: str
    isbn: str = Field(min_length=10, max_length=20)
    total_copies: int = Field(default=1, ge=1)


class BookCreate(BookBase):
    author_id: int


class BookUpdate(BaseModel):
    title: str | None = None
    total_copies: int | None = Field(default=None, ge=1)


class BookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    isbn: str
    total_copies: int
    available_copies: int
    author: AuthorRead
