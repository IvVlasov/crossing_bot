from repository.messages import MessagesRepository
from bot.services.weather_service import WeatherService
from repository import CrossingConfigRepository


class MessageService:
    start_user: str
    start_moderator: str
    message_types: str
    appeal_message: str
    appeal_message_success: str

    async def init_messages(self):
        messages = await MessagesRepository().get_messages()
        for message in messages:
            setattr(self, message.key, message.text)

    async def get_current_message(self) -> str:
        weather_service = WeatherService()
        crossing_config_repository = CrossingConfigRepository()
        crossing_config = await crossing_config_repository.get_crossing_config()
        weather_text = await weather_service.get_weather_text()
        text = f"Последнее сообщение о переправе 🗒:\n{crossing_config.last_message}\n\nПогода в районе ⛅️:\n{weather_text}"
        return text


async def get_message_service() -> MessageService:
    messages = MessageService()
    await messages.init_messages()
    return messages
