from pydantic import BaseModel, ConfigDict, EmailStr


class MemberBase(BaseModel):
    name: str
    email: EmailStr


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class MemberRead(MemberBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
