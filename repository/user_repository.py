from bot.models import User, NotificationType
from repository.base import BaseRepository


class UserRepository(BaseRepository):
    table_name = "users"

    async def create_table(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                chat_id BIGINT PRIMARY KEY
            )
        """
        await self.execute(create_table_query)

    async def create_user(self, user: User):
        await self.insert(**user.model_dump())

    async def get_user(self, chat_id: int) -> User | None:
        result = await self.select_one(chat_id=chat_id)
        return User(**result) if result else None

    async def update_user(self, chat_id: int, **kwargs):
        await self.update(
            set_conditions=kwargs,
            chat_id=chat_id,
        )

    async def get_all_users(self) -> list[User]:
        result = await self.select_all()
        return [User(**row) for row in result]
