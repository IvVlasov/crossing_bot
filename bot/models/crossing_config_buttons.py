from pydantic import BaseModel
from bot.models.crossing_config import CrossingMode


class CrossingConfigButtons(BaseModel):
    id: int | None = None
    button_name: str
    button_value: str
    crossing_mode: CrossingMode
