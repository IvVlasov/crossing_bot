from repository import UserRepository, UserNoticeRepository
from bot.app import bot
import logging
from aiogram.exceptions import TelegramForbiddenError
from openpyxl import Workbook
from io import BytesIO
from aiogram.types import BufferedInputFile
from datetime import datetime
import string


logger = logging.getLogger(__name__)


class StatisticService:

    def __init__(self):
        self.user_repository = UserRepository()
        self.user_notice_repository = UserNoticeRepository()
        self.bot = bot

    async def get_statistics_excel_file(self):
        is_blocked = 0

        # All users
        users = await self.user_repository.get_all_users()
        
        # Blocked users
        for user in users:
            if await self._check_user_blocked_bot(user.chat_id):
                is_blocked += 1

        # Users with notification type
        users_with_notification_type = await self.user_notice_repository.get_all_users_with_notification_type()
        statistics = {
            "Всего пользователей": len(users),
            "Блокированных пользователей": is_blocked,
            "Пользователей с уведомлениями": len(users_with_notification_type),
        }
        return await self._create_excel_file(statistics)

    async def _check_user_blocked_bot(self, chat_id: int) -> bool:
        try:
            await self.bot.send_chat_action(chat_id, 'typing', request_timeout=1)
            return False
        except TelegramForbiddenError:
            return True
        except Exception as e:
            logger.error(f'User {chat_id} blocked bot: {e}')
            return False

    async def _create_excel_file(self, statistics: dict):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Статистика"
        c = 0
        for key, value in statistics.items():
            letter = string.ascii_uppercase[c]
            sheet[f"{letter}1"] = key
            sheet[f"{letter}2"] = value
            sheet.column_dimensions[letter].width = 35
            c += 1
        buffer = BytesIO()
        workbook.save(buffer)
        buffer.seek(0)
        file_name = f"{datetime.now().strftime('%Y-%m-%d')}_statistic.xlsx"
        return BufferedInputFile(buffer.read(), filename=file_name)
