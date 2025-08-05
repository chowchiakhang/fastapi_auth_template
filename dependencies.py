from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlmodel import select

from database_engine.postgres_engine import SessionDep
from routers.users.schema import TokenData, User
from security.context import decode


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$B3ilkC1/HxDjV0ETDZZd1OihrRZWC1tIpsyCP2EpKqvTNro3yiy.i",
        "disabled": False,
    }
}

def get_user(session: SessionDep, username: str):
    statement = select(User).where(User.username == username)
    session_user = session.exec(statement).first()
    return session_user

async def get_current_user(session: SessionDep, token: Annotated[User, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(session, token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user
