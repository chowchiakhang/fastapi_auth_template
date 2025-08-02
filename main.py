from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from database_engine.postgres_engine import create_db_and_tables
from routers.auth.router import router as auth_router
from routers.users.router import router as users_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    # Cleanup code can be added here if needed

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)