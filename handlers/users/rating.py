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

        extract = extracter(datas=today_rating, delimiter=10)

        current_page = 1
        all_pages = len(extract)

        result = str()
        for student in extract[0]:
            result += (f"👤 Foydalanuvchi: {student['full_name']}\n"
                       f"📘 Test: {student['name']}\n"
                       f"✅ To'g'ri: {student['correct']}\n"
                       f"❌ Noto'g'ri: {student['incorrect']}\n\n")

        await message.answer(text=f"🏁 Bugungi natijalar:\n\n{result}\n",
                             reply_markup=key_returner(current_page=current_page, all_pages=all_pages))
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
    await process_results_page(call=call, direction="prev")


@dp.callback_query_handler(F.data.startswith("next_all:"))
async def handle_next_all(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await process_results_page(call=call, direction="next")
