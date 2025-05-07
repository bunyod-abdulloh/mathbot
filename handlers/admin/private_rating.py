from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from loader import dp
from states.admin import AdminStates


@dp.message_handler(IsBotAdminFilter(), F.text == "", state="*")
async def handle_admin_private_rating(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Foydalanuvchi ism familiyasini kiriting")
    await AdminStates.GET_FULL_NAME.set()


@dp.message_handler(state=AdminStates.GET_FULL_NAME, content_types=types.ContentType.TEXT)
async def handle_admin_get_fullname(message: types.Message, state: FSMContext):
    full_name = message.text


