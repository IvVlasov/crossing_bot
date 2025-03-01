from repository.base import BaseRepository
from bot.models.messages import Message


class MessagesRepository(BaseRepository):
    table_name = "messages"

    async def create_table(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL UNIQUE,
                text TEXT NOT NULL
            )
        """
        await self.execute(create_table_query)
        await self.insert(
            id=1,
            key="start_user",
            name="Стартовое сообщение пользователя",
            text="Вас приветствует официальный бот Переправы Салехард - Лабытнанги. Выберите необходимый пункт \"Меню\" или отправьте  команду /menu если меню не отобразилось",
        )
        await self.insert(
            id=2,
            key="start_moderator",
            name="Стартовое сообщение модератора",
            text="Вас приветствует официальный бот Переправы Салехард - Лабытнанги. Выберите необходимый пункт \"Меню\" или отправьте  команду /menu всли меню не отобразилось:",
        )
        await self.insert(
            id=3,
            key="message_types",
            name="Тип сообщения",
            text="Выберите тип сообщения:",
        )
        await self.insert(
            id=4,
            key="appeal_message",
            name="Обращение ввод",
            text="Введите текст вашего обращения.", 
        )
        await self.insert(
            id=5,
            key="appeal_message_success",
            name="Обращение принято",
            text="Ваше обращение принято.",
        )

    async def create_message(self, message: Message):
        await self.insert(
            key=message.key,
            name=message.name,
            text=message.text,
        )
        await self.update(
            set_conditions={
                "name": message.name,
                "text": message.text,
            },
            key=message.key,
        )

    async def get_messages(self) -> list[Message]:
        messages = await self.select_all()
        return [Message(**message) for message in messages]
