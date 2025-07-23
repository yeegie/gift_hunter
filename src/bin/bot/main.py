import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from app.handlers import routers

from app.infrastructure.bootstrap.runner import init_app
from app.infrastructure.config import RootConfig
from app.utils.ioc import ioc

from logging import Logger

from app.middlewares.manage_users import ManageUserMiddleware

from app.gift_service import GiftObserver, GiftNotifyer, GiftBuyer
from app.services.user.user import UserService

from app.adapters.session_creator import SqlalchemySessionCreator
from app.utils.database.create_schemas import generate_schema_from_session


async def on_startup(bot: Bot, dispatcher: Dispatcher):
    logger = ioc.get(Logger)
    logger.info('[📦] Launching the bot...')

    config = ioc.get(RootConfig)

    # Create schemas
    await generate_schema_from_session(ioc.get(SqlalchemySessionCreator).get_engine)

    # Webhook setup
    await bot.set_webhook(f'{config.webhook.base_url}{config.webhook.bot_path}')

    # Middleware setup
    dispatcher.message.outer_middleware(ManageUserMiddleware())
    dispatcher.callback_query.outer_middleware(ManageUserMiddleware())
    logger.info(f'[X] Middlewares included')

    # Include routers
    dispatcher.include_router(routers.user_router)
    dispatcher.include_router(routers.admin_router)
    dispatcher.include_router(routers.payment_router)
    logger.info(f'[X] Routers included')

    # Final log
    logger.info(f'[!] Bot stated -- https://t.me/{(await bot.get_me()).username}')

    # Notify owner
    await bot.send_message(423420323, "⚙️ Бот запущен")


async def on_shutdown(bot: Bot):
    ioc.get(Logger).info('[X] Stopping bot...')
    await bot.delete_webhook()


def main():
    init_app(
        webhook_config_path="configs/webhook.yml",
        telegram_config_path="configs/telegram.yml",
        database_config_path="configs/database.yml",
    )

    config = ioc.get(RootConfig)

    properties = DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    )

    bot = Bot(
        token=config.telegram.token.get_secret_value(),
        default=properties,
    )

    # Gift
    logger = ioc.get(Logger)

    gift_notifyer = GiftNotifyer(bot, user_service=ioc.get(UserService))
    gift_observer = GiftObserver(bot, gift_notifyer, logger)
    gift_buyer = GiftBuyer(bot, gift_observer, logger)

    ioc.set(GiftBuyer, gift_buyer)
    ioc.set(GiftObserver, gift_observer)

    storage = MemoryStorage()
    dispatcher = Dispatcher(storage=storage)

    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)

    app = web.Application()
    request_handler = SimpleRequestHandler(
        dispatcher,
        bot,
    )

    request_handler.register(app, path=config.webhook.bot_path)
    setup_application(app, dispatcher, bot=bot)

    web.run_app(app, host=config.webhook.listen_address,
                port=config.webhook.listen_port)


if __name__ == "__main__":
    main()
