from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from bot.handlers.filter import ModeratorFilter

from bot.constants import ModeratorMenuButtons, UserMenuButtons
from bot.models.crossing_config import CrossingConfig
from aiogram import types
from bot.constants.base import AppStringEnum
from bot.models.camera import Camera
from bot.models.user_notice import UserNotice, NotificationType
from bot.models.crossing_config import CrossingMode
from bot.models.crossing_config_buttons import CrossingConfigButtons
from bot.services.contact_service import ContactService


crossings_types = {
    CrossingMode.SUMMER: "Летний",
    CrossingMode.WINTER: "Зимний",
    CrossingMode.INTERSEASON: "Межсезонье",
}


def admin_menu_keyboard(crossing_config: CrossingConfig):
    builder = InlineKeyboardBuilder()
    for k, v in crossings_types.items():
        txt = "✅" if k == crossing_config.crossing_mode == k else "❌"
        builder.button(text=f"{v} {txt}", callback_data=f"set_crossing_type_{k}")
    builder.button(text="Файл настроек", callback_data="settings")
    builder.button(text="Статистика", callback_data="statistics")
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard


async def user_menu_keyboard(message: types.Message):
    moderator_filter = ModeratorFilter()
    is_moderator = await moderator_filter(message)
    contact_service = ContactService()
    contact_crossing_config_btn = await contact_service.get_contact_crossing_config_btn()
    is_contact_enabled = contact_crossing_config_btn is not None
    if is_moderator:
        return manager_menu_keyboard(is_contact_enabled)
    builder = ReplyKeyboardBuilder()

    for button in UserMenuButtons:
        if button == UserMenuButtons.CONTACTS:
            if is_contact_enabled:
                builder.button(text=button.value)
        else:
            builder.button(text=button.value)
    builder.adjust(1)
    keyboard = builder.as_markup()
    keyboard.resize_keyboard = True
    keyboard.one_time_keyboard = True
    return keyboard


def manager_menu_keyboard(is_contact_enabled: bool):
    builder = ReplyKeyboardBuilder()
    for button in ModeratorMenuButtons:
        if button == ModeratorMenuButtons.CONTACTS:
            if is_contact_enabled:
                builder.button(text=button.value)
        else:
            builder.button(text=button.value)
    builder.adjust(1)
    keyboard = builder.as_markup()
    keyboard.resize_keyboard = True
    keyboard.one_time_keyboard = True
    return keyboard


def user_cameras_keyboard(cameras: list[Camera]):
    builder = InlineKeyboardBuilder()
    for camera in cameras:
        builder.button(text=f"{camera.num}. {camera.name}", callback_data=f"get_camera_{camera.id}")
    builder.button(text="Назад", callback_data="back_to_user_menu")
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard


def user_crossing_config_links(crossing_config_buttons: list[CrossingConfigButtons]):
    builder = InlineKeyboardBuilder()
    for button in crossing_config_buttons:
        if button.button_value.startswith("http"):
            builder.button(text=button.button_name, url=button.button_value)
        else:
            builder.button(text=button.button_name, callback_data=f"send_cros_btn_message_{button.id}")
    builder.button(text="Назад", callback_data="back_to_user_menu")
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard


def notification_time_keyboard(user_notices: list[UserNotice]):
    user_notice_types = [user_notice.notification_type for user_notice in user_notices]
    builder = InlineKeyboardBuilder()
    for user_notice in NotificationType:
        emoji = "✅" if user_notice in user_notice_types else ""
        builder.button(text=f"{user_notice.ru_name} {emoji}", callback_data=f"{user_notice.value}")
    builder.button(text="Отписаться от всех уведомлений", callback_data="unsubscribe_from_all_notices")
    builder.button(text="Назад", callback_data="back_to_user_menu")
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard


def _inline_keyboard(keys: AppStringEnum):
    builder = InlineKeyboardBuilder()
    for key in keys:
        builder.button(text=key.value, callback_data=f"{key.name}")
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard


def _keyboard(keys: AppStringEnum):
    builder = ReplyKeyboardBuilder()
    for key in keys:
        builder.button(text=key.value)
    builder.adjust(1)
    keyboard = builder.as_markup()
    keyboard.resize_keyboard = True
    keyboard.one_time_keyboard = True
    return keyboard
