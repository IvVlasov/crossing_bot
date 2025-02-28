from bot.constants.base import AppStringEnum


class UserMenuButtons(AppStringEnum):
    STATE_NOW = "Текущая информация о переправе"
    ALLOW_NOTICES = "Подключить уведомления"
    CAMERAS = "Онлайн камеры"
    HELP = "Техподдержка"


class ModeratorMenuButtons(AppStringEnum):
    ADMINISTRATION = "Администрирование"
    STATE_NOW = "Текущая информация о переправе"
    ALLOW_NOTICES = "Подключить уведомления"
    CAMERAS = "Онлайн камеры"
    HELP = "Техподдержка"


class ModeratorCrossingButtons(AppStringEnum):
    WINTER_CROSSING = "Зимняя переправа (ледовая переправа)"
    SUMMER_CROSSING = "Летняя переправа (паромная переправа)"
    INTERSEASON_CROSSING = "Межсезонье (распутица)"


class NotificationTimeButtons(AppStringEnum):
    MORNING_MESSAGE = "Уведомлять в 06:00"
    EVENING_MESSAGE = "Уведомлять в 17:00"
    ALL_MESSAGES = "Подписаться на все уведомления (когда происходят изменения)"
    UNSUBSCRIBE_FROM_ALL_MESSAGES = "Отписаться от всех уведомлений"
    BACK_TO_USER_MENU = "Назад"


class ModeratorMessageTypes(AppStringEnum):
    MORNING_MESSAGE = "Ежедневное утренее сообщение"
    CLOSING_MESSAGE = "Сообщение о закрытии переправы"
    OPENING_MESSAGE = "Сообщение об открытии переправы"
    PASSENGER_TRAIN = "Пробный пассажирский рейс"
    LIMIT_MESSAGE = "Сообщение об ограничении"
