import asyncio

from repository.appeal_repository import AppealRepository
from repository.base import BaseRepository
from repository.cameras_repository import CamerasRepository
from repository.user_repository import UserRepository
from repository.messages import MessagesRepository
from repository.crossing_config_repository import CrossingConfigRepository
from repository.user_notice_repository import UserNoticeRepository
from repository.templates_repository import TemplatesRepository


async def create_tables():
    for child in BaseRepository.__subclasses__():
        await child().create_table()


asyncio.run(create_tables())
__all__ = [
    "UserRepository",
    "AppealRepository",
    "CamerasRepository",
    "BaseRepository",
    "MessagesRepository",
    "TemplatesRepository",
    "CrossingConfigRepository",
    "UserNoticeRepository",
]
