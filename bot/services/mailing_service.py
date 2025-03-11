from repository import UserRepository, UserNoticeRepository, CrossingConfigRepository
from bot.services.weather_service import WeatherService
from settings import get_settings
from bot.app import bot
from bot.models import NotificationType
from bot.services.message_service import get_message_service
from bot.models.crossing_config import CrossingMode


class MailingService:

    def __init__(self):
        self.user_repository = UserRepository()
        self.user_notice_repository = UserNoticeRepository()
        self.weather_service = WeatherService()
        self.crossing_config_repository = CrossingConfigRepository()
        self.settings = get_settings()

    async def _get_msg(self):
        crossing_config = await self.crossing_config_repository.get_crossing_config()
        if crossing_config.crossing_mode == CrossingMode.WINTER:
            return "На Ямале прогнозируют усиление ветра и метель. Возможно ограничение движения по ледовой переправе Салехард-Лабытнанги вплоть до закрытия."
        elif crossing_config.crossing_mode == CrossingMode.SUMMER:
            return "Возможно ограничение в работе паромной переправы, вплоть до полного прекращения движения. Рекомендуем следить за погодой и планировать поездки заранее."
        else:
            return "Возможны ограничения работы судов на воздушной подушке. Рекомендуем следить за погодой и планировать поездки заранее."

    async def check_weather(self):
        current_weather = await self.weather_service.get_current_weather()
        if self.settings.WIND_SPEED_LIMIT < current_weather.wind_speed_ms:
            users = await self.user_repository.get_all_users()
            for user in users:
                text = await self._get_msg()
                await bot.send_message(user.chat_id, text)

        if self.settings.VISIBILITY_LIMIT > current_weather.visibility:
            users = await self.user_repository.get_all_users()
            for user in users:
                text = await self._get_msg()
                await bot.send_message(user.chat_id, text)

    async def send_notification(self, notification_type: NotificationType):
        message_service = await get_message_service()
        users = await self.user_notice_repository.get_users_with_notification_type(notification_type)
        for user in users:
            text = await message_service.get_current_message()
            await bot.send_message(user.chat_id, text)
