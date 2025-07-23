__all__ = ["init_app"]

import asyncio

import logging
from app.infrastructure.bootstrap.config import get_config
from app.infrastructure.config import RootConfig

from app.adapters.session_creator import SqlalchemySessionCreator
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user.repository import UserRepository
from app.services.user.user import UserService

from app.utils.ioc import ioc


def init_app(
    telegram_config_path: str,
    database_config_path: str,
    webhook_config_path: str,
) -> None:
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    # Config
    config = get_config(
        telegram_config=telegram_config_path,
        database_config=database_config_path,
        webhook_config=webhook_config_path,
    )

    session_creator = SqlalchemySessionCreator((
        f"{config.database.driver}://"
        f"{config.database.user}:{config.database.password.get_secret_value()}"
        f"@{config.database.host}:{config.database.port}"
        f"/{config.database.database}"
    ), echo=True)
    session = session_creator.create_session()

    # Repositories
    user_repository = UserRepository(session, logger)

    # Services
    user_service = UserService(user_repository)

    # Store in IOC
    ioc.set(logging.Logger, logger)
    ioc.set(RootConfig, config)
    ioc.set(AsyncSession, session)
    ioc.set(SqlalchemySessionCreator, session_creator)
    ioc.set(UserRepository, user_repository)
    ioc.set(UserService, user_service)
