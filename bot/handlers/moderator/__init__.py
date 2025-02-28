from aiogram import Router

from bot.handlers.moderator.menu import menu_router


moderator_router = Router()


moderator_router.include_router(menu_router)

__all__ = ["moderator_router"]
