import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

logger = logging.getLogger(__name__)


class FirstOuterMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:

        logger.debug(
            'Вошли в миддлварь %s, тип события %s',
            __class__.__name__,
            event.__class__.__name__
        )

        result = await handler(event, data)

        logger.debug('Выходим из миддлвари  %s', __class__.__name__)

        return result


class SecondOuterMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        logger.debug(
            "Вошли в миддлварь %s, тип события %s",
            __class__.__name__,
            event.__class__.__name__,
        )

        result = await handler(event, data)

        logger.debug("Выходим из миддлвари  %s", __class__.__name__)

        return result


class ThirdOuterMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        logger.debug(
            "Вошли в миддлварь %s, тип события %s",
            __class__.__name__,
            event.__class__.__name__,
        )

        result = await handler(event, data)

        logger.debug("Выходим из миддлвари  %s", __class__.__name__)

        return result


class TranslatorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:

        user: User = data.get("event_from_user")

        if user is None:
            return await handler(event, data)

        user_lang = user.language_code
        # logger.debug(f'language user - {user_lang}')
        translations = data.get("translations")

        i18n = translations.get(user_lang)
        if i18n is None:
            data["i18n"] = translations[translations["default"]]
        else:
            data["i18n"] = i18n

        return await handler(event, data)