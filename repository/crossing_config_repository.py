from repository.base import BaseRepository
from bot.models.crossing_config import CrossingConfig, CrossingMode
from datetime import datetime


class CrossingConfigRepository(BaseRepository):
    table_name = "crossing_config"

    async def create_table(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY,
                last_message TEXT,
                crossing_mode TEXT,
                last_message_date TEXT
            )
        """
        await self.execute(create_table_query)
        await self.insert(id=1,
                          last_message="Пустое сообщение",
                          crossing_mode=CrossingMode.SUMMER,
                          last_message_date=datetime.now().strftime("%d.%m.%Y %H:%M"))

    async def update_crossing_config(self, **kwargs):
        await self.update(
            set_conditions=kwargs,
            id=1,
        )

    async def get_crossing_config(self) -> CrossingConfig:
        client_config = await self.select_one(id=1)
        return CrossingConfig(**client_config)
