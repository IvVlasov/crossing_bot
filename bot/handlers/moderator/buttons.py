from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.constants.base import AppStringEnum


def winter_crossing_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="30 тонн", callback_data="winter_crossing_30")
    builder.button(text="25 тонн", callback_data="winter_crossing_25")
    builder.button(text="15 тонн", callback_data="winter_crossing_15")
    builder.button(text="5 тонн", callback_data="winter_crossing_5")
    builder.button(text="3,5 тонны", callback_data="winter_crossing_3_5")
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
