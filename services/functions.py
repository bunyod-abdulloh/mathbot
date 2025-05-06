from aiogram import types

from keyboards.inline.users_ikb import key_returner
from loader import bot, stdb


def extracter(datas, delimiter):
    empty_list = []
    for e in range(0, len(datas), delimiter):
        empty_list.append(datas[e:e + delimiter])
    return empty_list


async def send_results_page(call: types.CallbackQuery, current_page, all_pages, extract_datas):
    try:
        extract = extracter(datas=extract_datas, delimiter=50)

        current_datas = extract[current_page] - 1

        result = str()
        your_result = "Siz to'plagan ball: "
        for student in current_datas:
            full_name = (await bot.get_chat(chat_id=student['telegram_id'])).full_name
            result += f"{student['row_num']}. {full_name} - {student['total_correct']} ball\n"
            if student['telegram_id'] == call.from_user.id:
                your_result += f"{student['total_correct']} ball"
        await call.message.edit_text(text=f"Umumiy natija:\n\n{result}\n{your_result}",
                                     reply_markup=key_returner(current_page=current_page, all_pages=all_pages))
        await call.answer(cache_time=0)

    except Exception as err:
        await call.answer(text=f"Xatolik: {err}", show_alert=True)


async def process_results_page(call: types.CallbackQuery, direction: str):
    all_students = await stdb.get_all_rating()

    extract = extracter(datas=all_students, delimiter=50)
    current_page = int(call.data.split(":")[1])
    all_pages = len(extract)

    if direction == "prev":
        current_page = current_page - 1 if current_page > 1 else all_pages
    elif direction == "next":
        current_page = current_page + 1 if current_page < all_pages else 1

    extracted_datas = extract[current_page - 1]

    await send_results_page(call=call, current_page=current_page, all_pages=all_pages, extract_datas=extracted_datas)
