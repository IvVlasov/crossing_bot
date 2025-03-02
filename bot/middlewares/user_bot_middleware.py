from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from settings import get_settings


class UserBotMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        settings = get_settings()
        if event.chat.id == settings.CHANNEL_ID:
            if event.reply_to_message:
                return await handler(event, data)
            else:
                return
        return await handler(event, data)


class UserBotMiddlewareCallback(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        settings = get_settings()
        if event.message.chat.id == settings.CHANNEL_ID:
            if event.message.reply_to_message:
                return await handler(event, data)
            else:
                return
        return await handler(event, data)
