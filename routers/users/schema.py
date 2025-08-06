from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str | None = None

class TokenData(BaseModel):
    username: str | None = None
