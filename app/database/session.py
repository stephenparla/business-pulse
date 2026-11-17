from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from app.database import engine

# Generate the async session factory
SessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# The dependency injected into endpoints
async def get_db():
    async with SessionLocal() as session:
        yield session
