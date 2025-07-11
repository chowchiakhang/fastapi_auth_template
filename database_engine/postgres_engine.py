from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from database_engine.utils import get_postgres_url
from models.user import User


engine = create_engine(get_postgres_url())


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]