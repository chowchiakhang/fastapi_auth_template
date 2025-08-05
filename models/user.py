from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    password: str
    is_active: bool = False
