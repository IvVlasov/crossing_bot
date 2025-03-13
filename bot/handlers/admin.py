from aiogram import F, Router, types
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext

from bot import buttons
from bot.app import bot
from bot.services.parse_settings_excel import ExcelSettings
from settings import get_settings
from repository import CrossingConfigRepository

admin_router = Router()
settings = get_settings()


class AdminFilter(Filter):
    async def __call__(self, msg: types.Message | types.CallbackQuery) -> bool:
        if isinstance(msg, types.Message):
            return msg.chat.id == settings.ADMIN_CHAT_ID
        if isinstance(msg, types.CallbackQuery):
            return msg.message.chat.id == settings.ADMIN_CHAT_ID


@admin_router.message(AdminFilter(), F.text == "/admin")
async def admin(message: types.Message, state: FSMContext):
    crossing_config_repository = CrossingConfigRepository()
    crossing_config = await crossing_config_repository.get_crossing_config()
    btn = buttons.admin_menu_keyboard(crossing_config)
    await message.answer("Меню администратора", reply_markup=btn)


@admin_router.callback_query(AdminFilter(), F.data == "settings")
async def get_settings(callback: types.CallbackQuery, state: FSMContext):
    text = "Текущие настройки бота. Измените их в файле и отправьте его мне."
    parse_settings_excel = ExcelSettings()
    document_file = await parse_settings_excel.get_excel_file()
    await callback.message.answer_document(document=document_file, caption=text)


@admin_router.callback_query(AdminFilter(), F.data.startswith("set_crossing_type_"))
async def set_crossing_type(callback: types.CallbackQuery, state: FSMContext):
    crossing_mode = callback.data.split("_")[-1]
    crossing_config_repository = CrossingConfigRepository()
    cur_crossing_config = await crossing_config_repository.get_crossing_config()
    if cur_crossing_config.crossing_mode == crossing_mode:
        return
    await crossing_config_repository.update_crossing_config(crossing_mode=crossing_mode)
    crossing_config = await crossing_config_repository.get_crossing_config()
    btn = buttons.admin_menu_keyboard(crossing_config)
    await callback.message.edit_reply_markup(reply_markup=btn)


@admin_router.message(AdminFilter(), F.document)
async def get_settings(message: types.Message, state: FSMContext):
    file = await bot.get_file(message.document.file_id)
    await bot.download_file(file.file_path, settings.SETTINGS_FILE_PATH)
    parse_settings_excel = ExcelSettings()
    is_success, error_message = await parse_settings_excel.parse_and_save()
    if is_success:
        await message.answer("Настройки успешно обновлены", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer(f"Произошла ошибка при обновлении настроек\n\nОшибка: {error_message}",
                             reply_markup=types.ReplyKeyboardRemove())
