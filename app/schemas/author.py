from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    nationality: str | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: str | None = None
    nationality: str | None = None


class AuthorRead(AuthorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
