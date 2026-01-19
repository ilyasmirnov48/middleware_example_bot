import asyncio
import logging

from aiogram import Bot, Dispatcher
from config.config import Config, load_config
from handlers.other import other_router
from handlers.user import user_router
# from middlewares.inner import (
#     FirstInnerMiddleware,
#     SecondInnerMiddleware,
#     ThirdInnerMiddlesare
# )
from middlewares.outer import (
    FirstOuterMiddleware,
#     SecondOuterMiddleware,
#     ThirdOuterMiddlesare
)

logger = logging.getLogger(__name__)


async def main() -> None:

    config: Config = load_config()

    logging.basicConfig(
        level =logging.getLevelName(level=config.log.level),
        format=config.log.format,
    )

    bot = Bot(token=config.bot.token)
    dp = Dispatcher()

    dp.include_router(user_router)
    dp.include_router(other_router)

    dp.update.outer_middleware(FirstOuterMiddleware())

    await dp.start_polling(bot)


asyncio.run(main())