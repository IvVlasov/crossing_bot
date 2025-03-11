from bot.models.crossing_config import CrossingMode
from pydantic import BaseModel


class Template(BaseModel):
    id: int | None = None
    crossing_mode: CrossingMode
    button_name: str
    message: str
    buttons_list: str | None = None
