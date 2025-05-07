from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from loader import dp, stdb
from states.admin import AdminStates


@dp.message_handler(IsBotAdminFilter(), F.text == "😎 Shaxsiy", state="*")
async def handle_admin_private_rating(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Foydalanuvchi ism familiyasini kiriting")
    await AdminStates.GET_FULL_NAME.set()


@dp.message_handler(state=AdminStates.GET_FULL_NAME, content_types=types.ContentType.TEXT)
async def handle_admin_get_fullname(message: types.Message, state: FSMContext):
    full_name = message.text

    results = await stdb.get_student_rating_by_fullname(full_name=full_name)

    if results:
        result_str = str()
        for index, result in enumerate(results, start=1):
            result_str += f"{index}. {result['name']} | ✅ {result['correct']} ta, ❌ {result['incorrect']} ta\n"
        await message.answer(text=f"👤 Foydalanuvchi: {message.text}\n\n"
                                  f"📊 Natijalar:\n\n"
                                  f"{result_str}")

    elif not results:
        await message.answer(text="Natijalar topilmadi!")
    await state.finish()
