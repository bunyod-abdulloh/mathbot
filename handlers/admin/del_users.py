from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from loader import dp, udb
from states.admin import AdminStates


@dp.message_handler(IsBotAdminFilter(), F.text == "👤❌ Foydalanuvchini o‘chirish", state="*")
async def handle_delete_user(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="👤 Foydalanuvchi ismi va familiyasini kiriting")
    await AdminStates.DEL_USER.set()


@dp.message_handler(state=AdminStates.DEL_USER, content_types=types.ContentType.TEXT)
async def handle_del_user_st(message: types.Message, state: FSMContext):
    await state.finish()
    success = await udb.delete_user_by_fullname(full_name=message.text)
    if success:
        await message.answer(text="✅ Foydalanuvchi o‘chirildi.")
    else:
        await message.answer(text="❌ Bunday foydalanuvchi topilmadi.")
