# app/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel

from app.database import engine
from app.routers.business_router import router as business_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


app = FastAPI(title="Business Pulse API", lifespan=lifespan)

# Register our business endpoint definitions
app.include_router(business_router)


@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Welcome to the Business Pulse API"
    }
