from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.constants.base import AppStringEnum
from bot.models.template import Template


def current_time_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Текущее время")
    builder.adjust(1)
    keyboard = builder.as_markup()
    keyboard.resize_keyboard = True
    keyboard.one_time_keyboard = True
    return keyboard


def get_buttons_keyboard(buttons: list[Template]):
    builder = InlineKeyboardBuilder()
    for button in buttons:
        builder.button(text=button.button_name, callback_data=f"select_template_{button.id}")
    builder.button(text="Назад", callback_data="back_to_user_menu")
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard


def get_buttons_keyboard_for_template(buttons: list[str]):
    builder = InlineKeyboardBuilder()
    for button in buttons:
        builder.button(text=button, callback_data=f"select_param_{button.strip()}")
    builder.button(text="Назад", callback_data="back_to_user_menu")
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard


def confirm_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Подтвердить", callback_data="confirm_yes")
    builder.button(text="Отменить", callback_data="confirm_no")
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


def _inline_keyboard(keys: AppStringEnum):
    builder = InlineKeyboardBuilder()
    for key in keys:
        builder.button(text=key.value, callback_data=f"{key.name}")
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard
