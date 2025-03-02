from repository import UserRepository, UserNoticeRepository
from bot.services.weather_service import WeatherService
from settings import get_settings
from bot.app import bot
from bot.models import NotificationType
from bot.services.message_service import get_message_service


class MailingService:

    def __init__(self):
        self.user_repository = UserRepository()
        self.user_notice_repository = UserNoticeRepository()
        self.weather_service = WeatherService()
        self.settings = get_settings()

    async def check_weather(self):
        current_weather = await self.weather_service.get_current_weather()
        print(current_weather)
        if self.settings.WIND_SPEED_LIMIT < current_weather.wind_speed_ms:
            users = await self.user_repository.get_all_users()
            for user in users:
                text = "Запрещено движения пассажирских судов в связи с сильным ветром. "
                await bot.send_message(user.chat_id, text)

        if self.settings.VISIBILITY_LIMIT > current_weather.visibility:
            users = await self.user_repository.get_all_users()
            for user in users:
                text = "Запрещено движения пассажирских судов в связи с плохой видимостью."
                await bot.send_message(user.chat_id, text)

    async def send_notification(self, notification_type: NotificationType):
        message_service = await get_message_service()
        users = await self.user_notice_repository.get_users_with_notification_type(notification_type)
        for user in users:
            text = await message_service.get_current_message()
            await bot.send_message(user.chat_id, text)
