from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.constants import ModeratorMenuButtons
from bot.handlers.filter import ModeratorFilter
from bot.handlers.moderator import buttons as moderator_buttons
from bot import buttons as user_buttons
from bot.handlers.moderator.states import SendMessageStates
from repository import CrossingConfigRepository, UserNoticeRepository, TemplatesRepository
from bot.models import NotificationType
from bot.app import bot
from datetime import datetime
from settings import get_settings


menu_router = Router()


@menu_router.message(ModeratorFilter(), F.text == ModeratorMenuButtons.ADMINISTRATION.value)
async def administration(message: types.Message, state: FSMContext):
    await state.set_state(SendMessageStates.crossing)
    crossing_config_repository = CrossingConfigRepository()
    crossing_config = await crossing_config_repository.get_crossing_config()
    templates_repository = TemplatesRepository()
    templates = await templates_repository.get_all_templates(crossing_config.crossing_mode)
    btn = moderator_buttons.get_buttons_keyboard(templates)
    text = "Выберите шаблон уведомления"
    await message.answer(text, reply_markup=btn)


async def send_preview_message(to_send: str, message: types.Message, state: FSMContext):
    await state.update_data(text_to_send=to_send)
    text = "Подтвердите отправку сообщения:\n\n"
    text = text + to_send
    await message.answer(text, reply_markup=moderator_buttons.confirm_keyboard())


@menu_router.callback_query(ModeratorFilter(), F.data.startswith("select_template_"), SendMessageStates.crossing)
async def choose_template(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    value = callback.data.split("_")[-1]
    templates_repository = TemplatesRepository()
    template = await templates_repository.get_template(id=value)
    await state.update_data(template=template)
    await state.set_state(SendMessageStates.template)
    if template.buttons_list == "время":
        text = 'Введите время в формате "12:00"'
        await callback.message.answer(text, reply_markup=moderator_buttons.current_time_keyboard())
    elif template.buttons_list:
        btn = moderator_buttons.get_buttons_keyboard_for_template(template.buttons_list.split(","))
        text = '\n\nВыберите вариант текста для заполнения шаблона'
        await callback.message.answer(template.message + text, reply_markup=btn)
    else:
        await state.update_data(template=template)
        await send_preview_message(template.message, callback.message, state)


@menu_router.message(ModeratorFilter(), SendMessageStates.template)
async def choose_time(message: types.Message, state: FSMContext):
    if message.text == "Текущее время":
        time = datetime.now().strftime("%H:%M")
    else:
        try:
            time = datetime.strptime(message.text, "%H:%M").strftime("%H:%M")
        except ValueError:
            await message.answer("Неверный формат времени. Введите время в формате '12:00'")
            return
    data = await state.get_data()
    template = data.get("template")
    text = template.message.replace("_", time)
    await send_preview_message(text, message, state)


@menu_router.callback_query(ModeratorFilter(), F.data.startswith("select_param_"), SendMessageStates.template)
async def choose_param(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    value = callback.data.split("_")[-1]
    data = await state.get_data()
    template = data.get("template")
    to_send = template.message.replace("_", value)
    await send_preview_message(to_send, callback.message, state)


@menu_router.callback_query(F.data == "confirm_yes")
async def close_crossing_message_confirm(callback: types.CallbackQuery, state: FSMContext):
    settings = get_settings()
    data = await state.get_data()
    text = data.get("text_to_send")
    crossing_config_repository = CrossingConfigRepository()
    await crossing_config_repository.update_crossing_config(last_message=text)
    user_notice_repository = UserNoticeRepository()
    users = await user_notice_repository.get_users_with_notification_type(NotificationType.ABOUT_LIMIT.value)
    for user in users:
        await bot.send_message(user.chat_id, text)
    await callback.message.delete()
    await state.clear()
    btn = await user_buttons.user_menu_keyboard(callback.message)
    await callback.message.answer("Сообщение отправлено", reply_markup=btn)
    manager_text = (
        "Пользователь ID: %s Username: @%s \nОтправил сообщение:\n\n%s"
    ) % (callback.message.chat.id, callback.message.chat.username, text)
    await bot.send_message(settings.MANAGER_CHAT_ID, manager_text)


@menu_router.callback_query(F.data == "confirm_no")
async def close_crossing_message_cancel(
    callback: types.CallbackQuery, state: FSMContext
):
    await callback.message.delete()
    await state.clear()
    btn = await user_buttons.user_menu_keyboard(callback.message)
    await callback.message.answer("Отправка сообщения отменена", reply_markup=btn)
