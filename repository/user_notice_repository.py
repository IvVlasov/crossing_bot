from bot.models import User, NotificationType
from repository.base import BaseRepository
from bot.models.user_notice import UserNotice


class UserNoticeRepository(BaseRepository):
    table_name = "user_notices"

    async def create_table(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                chat_id BIGINT,
                notification_type TEXT DEFAULT NULL
            )
        """
        await self.execute(create_table_query)

    async def create_user_notice(self, user_notice: UserNotice):
        await self.insert(**user_notice.model_dump())

    async def get_user_notices(self, chat_id: int) -> list[UserNotice]:
        result = await self.select_all(chat_id=chat_id)
        return [UserNotice(**row) for row in result]

    async def delete_user_notice(self, chat_id: int, notification_type: NotificationType):
        await self.delete(chat_id=chat_id, notification_type=notification_type)

    async def get_users_with_notification_type(self, notification_type: NotificationType) -> list[User]:
        result = await self.select_all(notification_type=notification_type)
        return [User(**row) for row in result]

    async def get_all_users_with_notification_type(self) -> list[User]:
        query = """SELECT distinct chat_id FROM user_notices"""
        result = await self.execute_fetchall(query)
        return [User(chat_id=row['chat_id']) for row in result]
