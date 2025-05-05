from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.users_ikb import user_main_ikb
from loader import dp, bks
from states.users import UserStates


@dp.message_handler(F.text == "✅ Javoblarni kiritish", state="*")
async def handle_user_main(message: types.Message, state: FSMContext):
    await state.finish()
    books = await bks.get_books()
    if not books:
        await message.answer(text="Hozircha testlar mavjud emas!")
    else:
        await message.answer(text="Javoblarni yuborish uchun testni tanlang",
                             reply_markup=user_main_ikb(books=books))


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
    book_id = data.get('user_book_id')

    # Ma'lumotlar bazasidan test uchun to'g'ri javoblarni olish
    correct_answers = await bks.get_correct_answers(book_id=book_id)
    len_answers = len(correct_answers)

    user_answers_text = message.text.strip().lower()
    user_answers = list(user_answers_text)

    # Javoblar soni tekshiriladi
    if len_answers != len(user_answers):
        await message.answer(
            text=f"Siz barcha savollarga javob bermadingiz!\n\nJami savollar soni: {len_answers} ta\n\n"
                 f"Siz yuborgan javoblar soni: {len(user_answers)} ta\n\nJavoblarni qayta yuboring")
        return

    # Javoblarni taqqoslash va natijani hisoblash
    correct_count = 0
    incorrect_count = 0
    result_details = ""

    for i, (user_answer, correct_answer) in enumerate(zip(user_answers, correct_answers), 1):

        if user_answer == correct_answer[0]:
            correct_count += 1
            result_details += f"    {i}. {user_answer.upper()}  ✅"
        else:
            incorrect_count += 1
            result_details += f"    {i}. {user_answer.upper()}  ❌ | ({correct_answer[0].upper()})  ✅"
        if i % 2 == 0:
            result_details += "\n\n"
    # Natijani xabar qilish
    await message.answer(
        text=f"<b>{message.from_user.full_name}</b> Siz bergan javoblar qabul qilindi.\n\nNatijangiz quyidagicha:\n\n"
             f"To'g'ri javoblar: {correct_count} ta\n"
             f"Noto'g'ri javoblar: {incorrect_count} ta\n\n"
             f"Javoblar tahlili:\n\n{result_details}"
    )

    # Natijani ma'lumotlar bazasiga saqlash (ixtiyoriy)
    # await bks.save_user_test_result(user_id=message.from_user.id, book_id=book_id,
    #                                correct=correct_count, incorrect=incorrect_count)

    # Keyingi holatga o'tkazish yoki joriy holatni tugatish
    await state.finish()
    # Yoki keyingi holatga o'tish
    # await UserStates.NEXT_STATE.set()
