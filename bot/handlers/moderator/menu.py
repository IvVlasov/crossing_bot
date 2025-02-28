from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.constants import ModeratorMenuButtons, ModeratorCrossingButtons
from bot.handlers.filter import ModeratorFilter
from bot.handlers.moderator import buttons as moderator_buttons
from bot import buttons as user_buttons
# from bot.handlers.moderator.states import SendMessageStates
# from repository import CrossingRepository, UserCrossingsRepository
# from bot.services.message_service import get_message_service
# from bot.app import bot
# from bot.buttons import _inline_keyboard


menu_router = Router()


@menu_router.message(ModeratorFilter(), F.text == ModeratorMenuButtons.ADMINISTRATION.value)
async def administration(message: types.Message, state: FSMContext):
    text = "Выберите переправу"
    btn = user_buttons._keyboard(ModeratorCrossingButtons)
    await message.answer(text, reply_markup=btn)


@menu_router.message(ModeratorFilter(), F.text == ModeratorCrossingButtons.WINTER_CROSSING.value)
async def winter_crossing(message: types.Message, state: FSMContext):
    # todo добавить сообщение в базу данных
    text = "Движение по ледовой переправе Салехард-Лабытнанги открыто для автомобилей массой до: "
    btn = moderator_buttons.winter_crossing_keyboard()
    await message.answer(text, reply_markup=btn)


@menu_router.callback_query(ModeratorFilter(), F.data.startswith("winter_crossing_"))
async def choose_winter_crossing(callback: types.CallbackQuery, state: FSMContext):
    # todo добавить сообщение в базу данных
    text = "Движение по ледовой переправе Салехард-Лабытнанги закрыто из-за неблагоприятных погодных условий"
    btn = moderator_buttons.confirm_keyboard()
    await callback.message.answer(text, reply_markup=btn)


@menu_router.message(ModeratorFilter(), F.text == ModeratorCrossingButtons.SUMMER_CROSSING.value)
async def summer_crossing(message: types.Message, state: FSMContext):
    pass


@menu_router.message(ModeratorFilter(), F.text == ModeratorCrossingButtons.INTERSEASON_CROSSING.value)
async def interseason_crossing(message: types.Message, state: FSMContext):
    pass


# @menu_router.callback_query(ModeratorFilter(), F.data.startswith("choose_crossing_"))
# async def choose_crossing(callback: types.CallbackQuery, state: FSMContext):
#     await callback.message.delete()
#     crossing_id = int(callback.data.split("_")[-1])
#     await state.set_state(SendMessageStates.crossing)
#     await state.update_data(crossing_id=crossing_id)
#     app_messages = await get_message_service()
#     await callback.message.answer(
#         app_messages.message_types,
#         reply_markup=buttons.send_message_types_keyboard(),
#     )


# @menu_router.callback_query(F.data == "confirm_yes")
# async def close_crossing_message_confirm(
#     callback: types.CallbackQuery, state: FSMContext
# ):
#     data = await state.get_data()
#     crossing_id = data.get("crossing_id")
#     user_crossings_repository = UserCrossingsRepository()
#     user_ids = await user_crossings_repository.get_user_crossings_by_ids(crossing_id)
#     for user_id in user_ids:
#         await bot.copy_message(user_id, callback.message.chat.id, data.get("message_id_to_send"))
#     await callback.message.delete()
#     await state.clear()
#     btn = await user_buttons.user_menu_keyboard(callback.message)
#     await callback.message.answer("Сообщение отправлено", reply_markup=btn)


# @menu_router.callback_query(F.data == "confirm_no")
# async def close_crossing_message_cancel(
#     callback: types.CallbackQuery, state: FSMContext
# ):
#     await callback.message.delete()
#     await state.clear()
#     btn = await user_buttons.user_menu_keyboard(callback.message)
#     await callback.message.answer("Отправка сообщения отменена", reply_markup=btn)
