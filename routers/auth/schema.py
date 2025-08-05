from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str

class UserRegistrationForm(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirmPassword: str

class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
