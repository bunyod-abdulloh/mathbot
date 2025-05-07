from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.users_ikb import key_returner
from loader import dp, stdb
from services.functions import extracter


@dp.message_handler(F.text == "🤗 Umumiy", state="*")
async def handle_admin_all_ratings(message: types.Message, state: FSMContext):
    try:
        await state.finish()
        all_students = await stdb.get_all_rating()

        extract = extracter(datas=all_students, delimiter=50)

        current_page = 1
        all_pages = len(extract)

        result = str()
        your_result = str()
        for student in extract[0]:
            result += f"🌟 {student['row_num']}. {student['full_name']} - {student['total_correct']} ball\n"
        await message.answer(text=f"📊 Umumiy natija:\n\n{result}",
                             reply_markup=key_returner(current_page=current_page, all_pages=all_pages,
                                                       your_result=your_result))
    except IndexError:
        await message.answer(text="Natijalarni ko'rsatish uchun birorta test javobi yuborilmagan!")
