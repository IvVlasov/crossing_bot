from pydantic import BaseModel, Field
from bot.constants.base import AppStringEnum


class CrossingMode(AppStringEnum):
    SUMMER = "summer"
    WINTER = "winter"
    INTERSEASON = "interseason"


class CrossingConfig(BaseModel):
    id: int = Field(default=1)
    last_message: str
    routing_link: str
    aviacommunication_link: str
    crossing_mode: CrossingMode
