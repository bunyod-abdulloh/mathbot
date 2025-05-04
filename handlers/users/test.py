from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from loader import dp, bks
from states.users import UserStates


@dp.callback_query_handler(F.data.startswith("user_test:"))
async def handle_user_test(call: types.CallbackQuery, state: FSMContext):
    book_id = int(call.data.split(":")[1])
    await state.update_data(user_book_id=book_id)
    book_name = await bks.get_book_name(book_id=book_id)

    await call.message.edit_text(text=f"Tanlangan test nomi: {book_name}\n\n"
                                      f"Javoblarni kiriting\n\n(javoblar faqat lotin harflarida kiritilishi lozim! katta "
                                      f"kichikligini ahamiyati yo'q):\n\n<b>Namuna: abcdabcdabcd</b>")
    await UserStates.GET_ANSWERS.set()


@dp.message_handler(state=UserStates.GET_ANSWERS, content_types=types.ContentType.TEXT)
async def handle_user_answers(message: types.Message, state: FSMContext):
    data = await state.get_data()
    len_answers = await bks.count_answers_on_book(book_id=data.get('user_book_id'))

    user_answers = list(message.text)

    if len_answers == len(user_answers):
        await message.answer(text="Javoblar qabul qilindi!")
    else:
        await message.answer(
            text=f"Siz barcha savollarga javob bermadingiz!\n\nJami savollar soni: {len_answers} ta\n\n"
                 f"Siz yuborgan javoblar soni: {len(user_answers)} ta\n\nJavoblarni qayta yuboring")
