from repository.base import BaseRepository
from bot.models.crossing_config_buttons import CrossingConfigButtons


class CrossingConfigButtonsRepository(BaseRepository):
    table_name = "crossing_config_buttons"

    async def create_table(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY,
                button_name TEXT,
                button_value TEXT,
                crossing_mode TEXT
            )
        """
        await self.execute(create_table_query)

    async def insert_crossing_config_button(self, crossing_config_button: CrossingConfigButtons):
        await self.insert(
            button_name=crossing_config_button.button_name,
            button_value=crossing_config_button.button_value,
            crossing_mode=crossing_config_button.crossing_mode,
        )

    async def get_crossing_config_button(self, id: int) -> CrossingConfigButtons:
        crossing_config_button = await self.select_one(id=id)
        return CrossingConfigButtons(**crossing_config_button)

    async def delete_all_crossing_config_buttons(self):
        await self.delete_all()

    async def get_crossing_config_buttons(self) -> list[CrossingConfigButtons]:
        crossing_config_buttons = await self.select_all()
        return [CrossingConfigButtons(**crossing_config_button) for crossing_config_button in crossing_config_buttons]
