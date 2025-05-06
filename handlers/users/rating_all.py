from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from loader import dp, stdb
from services.functions import process_results_page


@dp.message_handler(F.text == "🤗 Umumiy", state="*")
async def handle_rating_all(message: types.Message, state: FSMContext):
    await message.answer(text="Bo'lim ishga tushmadi!")

    # await state.finish()
    # all_students = await stdb.get_all_rating()
    # print(all_students)

    # extract = extracter(datas=all_students, delimiter=50)
    #
    # current_page = 1
    # all_pages = len(extract)
    #
    # result = str()
    # your_result = "Siz to'plagan ball: "
    # for student in extract[0]:
    #     full_name = (await bot.get_chat(chat_id=student['telegram_id'])).full_name
    #     result += f"{student['row_num']}. {full_name} - {student['total_correct']} ball\n"
    #     if student['telegram_id'] == message.from_user.id:
    #         your_result += f"{student['total_correct']} ball"
    # await message.answer(text=f"Umumiy natija:\n\n{result}\n{your_result}",
    #                      reply_markup=key_returner(current_page=current_page, all_pages=all_pages))


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
    print("next")
    await process_results_page(call=call, direction="next")


@dp.message_handler(F.text == "salom", state="*")
async def salomsalom(message: types.Message, state: FSMContext):
    for n in range(200):
        await stdb.add_example(full_name=f"Bunyod {n}", user_id=1, correct=n, incorrect=0)
