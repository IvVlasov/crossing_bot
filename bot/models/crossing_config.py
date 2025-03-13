from pydantic import BaseModel, Field
from bot.constants.base import AppStringEnum


class CrossingMode(AppStringEnum):
    SUMMER = "summer"
    WINTER = "winter"
    INTERSEASON = "interseason"

    @classmethod
    def get_crossing_mode_by_name(cls, in_val: int):
        if in_val == 0:
            return cls.SUMMER
        elif in_val == 1:
            return cls.WINTER
        elif in_val == 2:
            return cls.INTERSEASON
        else:
            raise ValueError(f"Invalid crossing mode: {in_val}")


class CrossingConfig(BaseModel):
    id: int = Field(default=1)
    last_message: str
    crossing_mode: CrossingMode
