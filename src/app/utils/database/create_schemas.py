from sqlalchemy.ext.asyncio import AsyncEngine
from app.repositories.models.base import Base


async def generate_schema_from_session(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
