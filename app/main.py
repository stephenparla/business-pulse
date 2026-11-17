# app/main.py

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from app.database import engine
from app.database.session import SessionLocal
from app.repositories.business_repository import seed_fictional_business_data
from app.routers.business_router import router as business_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with SessionLocal() as session:
        await seed_fictional_business_data(session)

    yield


app = FastAPI(title="Business Pulse API", lifespan=lifespan)

# Register our business endpoint definitions
app.include_router(business_router)


@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Welcome to the Business Pulse API",
    }
