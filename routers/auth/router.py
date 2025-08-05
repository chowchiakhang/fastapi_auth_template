from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from database_engine.postgres_engine import SessionDep
from dependencies import get_user
from models.user import User
from routers.auth.schema import Token, UserPublic, UserRegistrationForm
from security.context import create_access_token, get_password_hash, verify_password


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

def authenticate_user(session: SessionDep, username: str, password: str):
    user = get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

@router.post("/token")
async def login_for_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(session, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")

@router.post("/register", response_model=UserPublic) # response_model to marshal response
async def register_user(session: SessionDep, user_form: UserRegistrationForm):
    if user_form.password != user_form.confirmPassword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    if get_user(session, user_form.username) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    try:
        db_obj = User.model_validate({
            "username": user_form.username,
            "email": user_form.email,
            "password": get_password_hash(user_form.password),
            "is_active": True
        })
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    # TODO: send email
    return db_obj
