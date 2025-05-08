from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.users_ikb import key_returner
from loader import dp, stdb
from services.functions import extracter, process_results_page


@dp.message_handler(F.text == "📊 Natijalar", state="*")
async def handle_rating_all(message: types.Message, state: FSMContext):
    try:
        await state.finish()
        today_rating = await stdb.get_today_ratings()
        print(today_rating)
        all_students = await stdb.get_all_rating()

        extract = extracter(datas=all_students, delimiter=50)

        current_page = 1
        all_pages = len(extract)

        result = str()
        your_result = str()
        for student in extract[0]:
            result += (f"👤 {student['full_name']}\n"
                       f"{student['total_correct']} ball\n")
            # if student['telegram_id'] == message.from_user.id:
            #     your_result = student['total_correct']
        await message.answer(text=f"🏁 Bugungi natijalar:\n\n{result}\n📌 Siz to'plagan ball: {your_result} ball",
                             reply_markup=key_returner(current_page=current_page, all_pages=all_pages,
                                                       your_result=your_result))
    except IndexError:
        await message.answer(text="❗️ <b>Natijalarni ko'rsatish uchun birorta test joylanmagan!</b>")


@dp.callback_query_handler(F.data.startswith("alertall:"), state="*")
async def handle_alert_all(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    current_page = call.data.split(":")[1]
    await call.answer(text=f"Siz {current_page} - sahifadasiz!", show_alert=True)


@dp.callback_query_handler(F.data.startswith("prev_all:"))
async def handle_prev_all(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    your_result = call.data.split(":")[2]
    await process_results_page(call=call, direction="prev", your_result=your_result)


@dp.callback_query_handler(F.data.startswith("next_all:"))
async def handle_next_all(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    your_result = call.data.split(":")[2]
    await process_results_page(call=call, direction="next", your_result=your_result)
