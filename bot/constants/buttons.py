from bot.constants.base import AppStringEnum


class UserMenuButtons(AppStringEnum):
    STATE_NOW = "Текущая информация о переправе"
    ALLOW_NOTICES = "Подключить уведомления"
    CAMERAS = "Онлайн камеры"
    CONTACTS = "Контакты"
    HELP = "Техподдержка"


class ModeratorMenuButtons(AppStringEnum):
    ADMINISTRATION = "Администрирование"
    STATE_NOW = "Текущая информация о переправе"
    ALLOW_NOTICES = "Подключить уведомления"
    CAMERAS = "Онлайн камеры"
    CONTACTS = "Контакты"
    HELP = "Техподдержка"
