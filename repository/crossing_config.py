from repository.base import BaseRepository
from bot.models.crossing_config import CrossingConfig, CrossingMode


class CrossingConfigRepository(BaseRepository):
    table_name = "crossing_config"

    async def create_table(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY,
                last_message TEXT,
                routing_link TEXT,
                aviacommunication_link TEXT,
                crossing_mode VARCHAR(255)
            )
        """
        r = await self.execute(create_table_query)
        print('RESULTE', r)
        # await self.insert(id=1,
        #                   last_message="Пустое сообщение",
        #                   routing_link="https://www.google.com/",
        #                   aviacommunication_link="https://ya.ru/",
        #                   crossing_mode=CrossingMode.SUMMER)

    async def update_crossing_config(self, client_config: CrossingConfig):
        await self.update(
            set_conditions={
                "last_message": client_config.last_message,
                "routing_link": client_config.routing_link,
                "aviacommunication_link": client_config.aviacommunication_link,
            },
            id=1,
        )

    async def get_crossing_config(self) -> CrossingConfig:
        client_config = await self.select_one(id=1)
        return CrossingConfig(**client_config)
