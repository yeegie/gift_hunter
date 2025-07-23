from .SessionCreator import SessionCreator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker


class SqlalchemySessionCreator(SessionCreator):
    def __init__(self, db_uri: str, echo: bool = False) -> None:
        self._db_uri = db_uri
        self._engine = create_async_engine(self._db_uri, echo=echo)
        self._SessionLocal = sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    def create_session(self) -> AsyncSession:
        return self._SessionLocal()
    
    @property
    def get_engine(self) -> AsyncEngine:
        return self._engine
