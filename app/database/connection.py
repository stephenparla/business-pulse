import os
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://postgres@localhost:5432/bubblesort_pulse_dev"
)

# Core connection engine
engine = create_async_engine(DATABASE_URL, echo=True)
