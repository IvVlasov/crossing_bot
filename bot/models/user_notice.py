from pydantic import BaseModel
from bot.constants.base import AppStringEnum


class NotificationType(AppStringEnum):
    ABOUT_LIMIT = "about_limit"
    SIX_HOURS = "6_hours"
    SEVENTEEN_HOURS = "17_hours"
    ALL_NOTICES = "all_notices"

    @property
    def ru_name(self):
        if self == NotificationType.ABOUT_LIMIT:
            return "Об ограничениях"
        elif self == NotificationType.SIX_HOURS:
            return "Уведомлять в 06:00"
        elif self == NotificationType.SEVENTEEN_HOURS:
            return "Уведомлять в 17:00"
        elif self == NotificationType.ALL_NOTICES:
            return "Все уведомления"
        else:
            return self


class UserNotice(BaseModel):
    chat_id: int
    notification_type: NotificationType | None = None
