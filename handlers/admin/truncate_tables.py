from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from loader import dp, stdb


@dp.message_handler(IsBotAdminFilter(), F.text == "🧹 Jadvalni tozalash", state="*")
async def handle_truncate_table_ratings(message: types.Message, state: FSMContext):
    await state.finish()
    await stdb.clear_table_students()
    await message.answer(text="Jadval tozalandi! 🧹✅📁")
