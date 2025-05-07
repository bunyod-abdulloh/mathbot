from aiogram import types

from keyboards.inline.users_ikb import key_returner
from loader import stdb


def extracter(datas, delimiter):
    empty_list = []
    for e in range(0, len(datas), delimiter):
        empty_list.append(datas[e:e + delimiter])
    return empty_list


async def send_results_page(call: types.CallbackQuery, current_page, all_pages, extract_datas, your_result):
    await call.answer(cache_time=0)
    try:
        result = str()
        for student in extract_datas:
            result += f"{student['row_num']}. {student['full_name']} - {student['total_correct']} ball\n"
        if your_result:
            await call.message.edit_text(text=f"Umumiy natija:\n\n{result}\nSiz to'plagan ball: {your_result} ball",
                                         reply_markup=key_returner(current_page=current_page, all_pages=all_pages,
                                                                   your_result=your_result))
        else:
            await call.message.edit_text(text=f"Umumiy natija:\n\n{result}",
                                         reply_markup=key_returner(current_page=current_page, all_pages=all_pages,
                                                                   your_result=your_result))
    except Exception as err:
        await call.answer(text=f"Xatolik: {err}", show_alert=True)


async def process_results_page(call: types.CallbackQuery, direction: str, your_result):
    all_students = await stdb.get_all_rating()

    extract = extracter(datas=all_students, delimiter=50)
    current_page = int(call.data.split(":")[1])
    all_pages = len(extract)

    if direction == "prev":
        current_page = current_page - 1 if current_page > 1 else all_pages
    elif direction == "next":
        current_page = current_page + 1 if current_page < all_pages else 1

    extracted_datas = extract[current_page - 1]

    await send_results_page(call=call, current_page=current_page, all_pages=all_pages, extract_datas=extracted_datas,
                            your_result=your_result)
