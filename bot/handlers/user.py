from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from bot.handlers.states import NotificationStates

from bot import buttons
from bot.constants import UserMenuButtons
from bot.handlers.filter import ModeratorFilter
from bot.models import User, UserNotice
from bot.services.message_service import get_message_service
from repository import CrossingConfigRepository, UserRepository, CamerasRepository, UserNoticeRepository

user_router = Router()


@user_router.message(ModeratorFilter(), F.text.startswith("/start"))
async def start_moderator(message: types.Message, state: FSMContext):
    user_repository = UserRepository()
    await user_repository.create_user(User(chat_id=message.chat.id))
    app_messages = await get_message_service()
    text, btn = app_messages.start_moderator, await buttons.user_menu_keyboard(message)
    await message.answer(text, reply_markup=btn)
    await state.clear()


@user_router.message(F.text.startswith("/start"))
async def start(message: types.Message, state: FSMContext):
    user_repository = UserRepository()
    await user_repository.create_user(User(chat_id=message.chat.id))
    app_messages = await get_message_service()
    text, btn = app_messages.start_user, await buttons.user_menu_keyboard(message)
    text = text.format(user_name=message.from_user.full_name)
    await message.answer(text, reply_markup=btn)
    await state.clear()


@user_router.message(F.text == "Назад")
async def back_to_user_menu_reply(message: types.Message, state: FSMContext):
    app_messages = await get_message_service()
    text, btn = app_messages.start_user, await buttons.user_menu_keyboard(message)
    text = text.format(user_name=message.from_user.full_name)
    await message.answer(text, reply_markup=btn)
    await state.clear()


@user_router.callback_query(F.data == "back_to_user_menu")
async def back_to_user_menu(callback: types.CallbackQuery, state: FSMContext):
    app_messages = await get_message_service()
    text, btn = app_messages.start_user, await buttons.user_menu_keyboard(callback.message)
    await callback.message.answer(text, reply_markup=btn)
    await state.clear()


@user_router.message(F.text == UserMenuButtons.STATE_NOW.value)
async def state_now(message: types.Message, state: FSMContext, user: User):
    crossing_config_repository = CrossingConfigRepository()
    crossing_config = await crossing_config_repository.get_crossing_config()
    btn = buttons.user_crossing_config_links(crossing_config)
    await message.answer(crossing_config.last_message, reply_markup=btn)


@user_router.message(F.text == UserMenuButtons.ALLOW_NOTICES.value)
async def allow_notices(message: types.Message, state: FSMContext, user: User):
    user_notice_repository = UserNoticeRepository()
    user_notices = await user_notice_repository.get_user_notices(user.chat_id)
    await state.set_state(NotificationStates.notification_type)
    btn = buttons.notification_time_keyboard(user_notices)
    await message.answer("Включите или отключите уведомления", reply_markup=btn)


@user_router.callback_query(NotificationStates.notification_type)
async def notification_type(callback: types.CallbackQuery, state: FSMContext, user: User):
    user_notice_repository = UserNoticeRepository()
    current_user_notice = await user_notice_repository.get_user_notices(user.chat_id)
    current_user_notice_types = [user_notice.notification_type for user_notice in current_user_notice]

    match callback.data:
        case "unsubscribe_from_all_notices":
            for user_notice in current_user_notice:
                await user_notice_repository.delete_user_notice(user.chat_id, user_notice.notification_type)
        case _:
            if callback.data in current_user_notice_types:
                await user_notice_repository.delete_user_notice(user.chat_id, callback.data)
            else:
                await user_notice_repository.create_user_notice(
                    UserNotice(chat_id=user.chat_id, notification_type=callback.data)
                )

    user_notices = await user_notice_repository.get_user_notices(user.chat_id)
    btn = buttons.notification_time_keyboard(user_notices)
    await callback.message.edit_reply_markup(reply_markup=btn)


@user_router.message(F.text == UserMenuButtons.CAMERAS.value)
async def cameras(message: types.Message, state: FSMContext, user: User):
    cameras_repository = CamerasRepository()
    cameras = await cameras_repository.get_all_cameras()
    btn = buttons.user_cameras_keyboard(cameras)
    await message.answer("Выберите камеру", reply_markup=btn)
