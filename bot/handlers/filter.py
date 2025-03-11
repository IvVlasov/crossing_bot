from aiogram import types
from aiogram.filters import Filter

from bot.app import bot
from bot.constants.chat_members import ChatMemberStatus
from settings import get_settings


class ModeratorFilter(Filter):
    async def __call__(self, message: types.Message | types.CallbackQuery) -> bool:
        settings = get_settings()
        msg = message.message if isinstance(message, types.CallbackQuery) else message
        chat_member = await bot.get_chat_member(settings.CHANNEL_ID, msg.chat.id)
        return chat_member.status in [
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR,
            ChatMemberStatus.MEMBER,
        ]
