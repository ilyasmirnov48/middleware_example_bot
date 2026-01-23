import asyncio
import logging

from lexicon.lexicon_en import LEXICON_EN
from lexicon.lexicon_ru import LEXICON_RU
from middlewares.outer import TranslatorMiddleware
from aiogram import Bot, Dispatcher
from config.config import Config, load_config
from handlers.other import other_router
from handlers.user import user_router
# from middlewares.inner import (
#     FirstInnerMiddleware,
#     SecondInnerMiddleware,
#     ThirdInnerMiddleware
# )
from middlewares.outer import (
    TranslatorMiddleware,
#     FirstOuterMiddleware,
#     SecondOuterMiddleware,
#     ThirdOuterMiddleware
)

logger = logging.getLogger(__name__)


translations = {
    'default': 'en',
    'en': LEXICON_EN,
    'ru': LEXICON_RU,
}


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

    dp.update.middleware(TranslatorMiddleware())

    await dp.start_polling(bot, translations=translations)


asyncio.run(main())