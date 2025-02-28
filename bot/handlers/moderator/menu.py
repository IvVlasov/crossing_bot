from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.constants import ModeratorMenuButtons
from bot.handlers.filter import ModeratorFilter
from bot.handlers.moderator import buttons as moderator_buttons
from bot import buttons as user_buttons
from bot.handlers.moderator.states import SendMessageStates
from repository import CrossingConfigRepository, UserRepository
from bot.models.crossing_config import CrossingMode
from bot.models import NotificationType
# from bot.handlers.moderator.states import SendMessageStates
# from repository import CrossingRepository, UserCrossingsRepository
# from bot.services.message_service import get_message_service
from bot.app import bot
# from bot.buttons import _inline_keyboard


menu_router = Router()


@menu_router.message(ModeratorFilter(), F.text == ModeratorMenuButtons.ADMINISTRATION.value)
async def administration(message: types.Message, state: FSMContext):
    await state.set_state(SendMessageStates.crossing)
    crossing_config_repository = CrossingConfigRepository()
    crossing_config = await crossing_config_repository.get_crossing_config()
    match crossing_config.crossing_mode:
        case CrossingMode.WINTER:
            text = "Движение по ледовой переправе Салехард-Лабытнанги открыто для автомобилей массой до:"
            btn = moderator_buttons.winter_crossing_keyboard()
        case CrossingMode.SUMMER:
            text = "Переправа работает в обычном режиме, на линии _ паром(ов)"
            btn = moderator_buttons.summer_crossing_keyboard()
        case CrossingMode.INTERSEASON:
            text = "На линии работают суда на воздушной подушке, задействовано ___ единиц."
            btn = moderator_buttons.interseason_crossing_keyboard()
    await message.answer(text, reply_markup=btn)


@menu_router.callback_query(ModeratorFilter(), F.data.startswith("winter_crossing_"), SendMessageStates.crossing)
async def choose_winter_crossing(callback: types.CallbackQuery, state: FSMContext):
    value = callback.data.split("_")[-1]
    await state.update_data(winter_crossing_value=value)
    text = f"Движение по ледовой переправе Салехард-Лабытнанги открыто для автомобилей массой до: {value} тонн"
    btn = moderator_buttons.confirm_keyboard()
    await state.update_data(text_to_send=text)
    await callback.message.answer(text, reply_markup=btn)


@menu_router.callback_query(ModeratorFilter(), F.data.startswith("summer_crossing_"), SendMessageStates.crossing)
async def choose_summer_crossing(callback: types.CallbackQuery, state: FSMContext):
    value = callback.data.split("_")[-1]
    await state.update_data(summer_crossing_value=value)
    text = f"Переправа работает в обычном режиме, на линии {value} паром(ов)"
    btn = moderator_buttons.confirm_keyboard()
    await state.update_data(text_to_send=text)
    await callback.message.answer(text, reply_markup=btn)


@menu_router.callback_query(ModeratorFilter(), F.data.startswith("interseason_crossing_"), SendMessageStates.crossing)
async def choose_interseason_crossing(callback: types.CallbackQuery, state: FSMContext):
    value = callback.data.split("_")[-1]
    await state.update_data(interseason_crossing_value=value)
    text = f"На линии работают суда на воздушной подушке, задействовано {value} единиц."
    btn = moderator_buttons.confirm_keyboard()
    await state.update_data(text_to_send=text)
    await callback.message.answer(text, reply_markup=btn)


@menu_router.callback_query(F.data == "confirm_yes")
async def close_crossing_message_confirm(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text_to_send")
    crossing_config_repository = CrossingConfigRepository()
    await crossing_config_repository.update_crossing_config(last_message=text)
    user_repository = UserRepository()
    users = await user_repository.get_users_with_notification_type(NotificationType.ALL_NOTICES.value)
    for user in users:
        await bot.send_message(user.chat_id, text)
    await callback.message.delete()
    await state.clear()
    btn = await user_buttons.user_menu_keyboard(callback.message)
    await callback.message.answer("Сообщение отправлено", reply_markup=btn)


@menu_router.callback_query(F.data == "confirm_no")
async def close_crossing_message_cancel(
    callback: types.CallbackQuery, state: FSMContext
):
    await callback.message.delete()
    await state.clear()
    btn = await user_buttons.user_menu_keyboard(callback.message)
    await callback.message.answer("Отправка сообщения отменена", reply_markup=btn)
