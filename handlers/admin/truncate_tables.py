from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from keyboards.inline.admin_ikb import admin_clear_rating_ikb
from loader import dp, stdb


@dp.message_handler(IsBotAdminFilter(), F.text == "🧹 Jadvalni tozalash", state="*")
async def handle_truncate_table_ratings(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="📊 Natijalar jadvalini tozalashni istaysizmi?",
                         reply_markup=admin_clear_rating_ikb())


@dp.callback_query_handler(F.data == "admin_no", state="*")
async def handle_admin_no(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(text="⚠️ Buyruq bekor qilindi!")


@dp.callback_query_handler(F.data == "admin_yes", state="*")
async def handle_admin_yes(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await stdb.clear_table_students()
    await call.message.edit_text(text="Jadval tozalandi! 🧹✅📁")
