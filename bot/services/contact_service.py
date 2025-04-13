from repository.crossing_config_buttons_repository import CrossingConfigButtonsRepository
from repository.crossing_config_repository import CrossingConfigRepository
# from bot.models.crossing_config import CrossingConfig
from bot.models.crossing_config_buttons import CrossingConfigButtons
import re


class ContactService:

    def __init__(self):
        self.crossing_config_buttons_repository = CrossingConfigButtonsRepository()
        self.crossing_config_repository = CrossingConfigRepository()

    async def get_contact_crossing_config_btn(self) -> CrossingConfigButtons | None:
        crossing_config = await self.crossing_config_repository.get_crossing_config()
        crossing_config_buttons = await self.crossing_config_buttons_repository.get_crossing_config_buttons()
        for crossing_config_button in crossing_config_buttons:
            if (crossing_config_button.crossing_mode == crossing_config.crossing_mode and
                    crossing_config_button.button_name == "Контакты"):
                return crossing_config_button
        return None

    async def get_crossing_config_buttons(self) -> list[CrossingConfigButtons]:
        crossing_config = await self.crossing_config_repository.get_crossing_config()
        crossing_config_buttons = await self.crossing_config_buttons_repository.get_crossing_config_buttons()
        return [
            el for el in crossing_config_buttons if el.crossing_mode == crossing_config.crossing_mode
        ]

    async def get_html_btn_text(self, btn_id: int) -> str:
        crossing_config_button = await self.crossing_config_buttons_repository.get_crossing_config_button(btn_id)
        return re.sub(r'\[(.*?)\]\((.*?)\)', self._replacer, crossing_config_button.button_value)

    def _replacer(self, match):
        label = match.group(1)
        url = match.group(2)
        res = f'<a href="{url}">{label}</>'
        print(res)
        return res
