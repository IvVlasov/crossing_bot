from pydantic import BaseModel
from enum import Enum


class NotificationType(str, Enum):
    SIX_HOURS = "6_hours"
    SEVENTEEN_HOURS = "17_hours"
    ALL_NOTICES = "all_notices"


class User(BaseModel):
    chat_id: int
    notification_type: NotificationType | None = None
