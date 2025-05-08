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
            result += f"🌟 {student['row_num']}. {student['full_name']} - {student['total_correct']} ball\n"
        if your_result:
            await call.message.edit_text(text=f"🏁 Umumiy natija:\n\n{result}\n📌 Siz to'plagan ball: {your_result} ball",
                                         reply_markup=key_returner(current_page=current_page, all_pages=all_pages,
                                                                   your_result=your_result))
        else:
            await call.message.edit_text(text=f"🏁 Umumiy natija:\n\n{result}",
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


answer_text = "📝 Javoblarni yuborish uchun 📚 testni tanlang:"

no_test_text = ("🚫 <b>Hozircha testlar mavjud emas!</b>\n\n"
                "📌 Iltimos, keyinroq urinib ko‘ring yoki yangilanishlarni kuting!")

user_not_found_text = (
    "🚫 <b>Siz foydalanuvchilar ro‘yxatida topilmadingiz!</b>\n\n"
    "Iltimos, <b>/start</b> buyrug‘ini yuboring va botdan foydalanishni qayta boshlang. ✅"
)

enter_full_name_text = (
    "🖊️ <b>Ism familiyangizni kiriting:</b>\n\n"
    "📌 <i>Namuna:</i> <b>Mardon Mardonov</b>"
)


def test_input_prompt(book):
    text = (
        f"📘 <b>Test nomi:</b> {book['name']}\n\n"
        f"✍️ <b>Javoblaringizni kiriting</b>\n\n"
        f"🔤 Javoblar faqat <b>lotin harflarida</b> bo‘lishi lozim. "
        f"Katta-kichik harflar ahamiyatga ega emas.\n\n"
        f"📌 <i>Namuna:</i> <b>abcdabcdabcd</b>"
    )
    return text


def incomplete_answers_text(len_answers, user_answers):
    text = (
        f"⚠️ <b>Siz barcha savollarga javob bermadingiz!</b>\n\n"
        f"❓ <b>Jami savollar:</b> {len_answers} ta\n"
        f"✍️ <b>Siz yuborgan javoblar:</b> {len(user_answers)} ta\n\n"
        f"🔁 Iltimos, barcha javoblarni to‘liq kiriting va qayta yuboring."
    )
    return text
