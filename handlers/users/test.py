from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.users_ikb import user_main_ikb
from loader import dp, bks, udb, stdb
from states.users import UserStates


@dp.message_handler(F.text == "✅ Javoblarni kiritish", state="*")
async def handle_user_main(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = int(await udb.select_user(telegram_id=message.from_user.id))

    await state.update_data(student_user_id=user_id)
    if user_id:
        check_student = await stdb.check_student(user_id=user_id)
        print(check_student)
        if not check_student:
            await message.answer(text="Ism familiyangizni kiriting\n\n<b>Namuna: Mardon Mardonov</b>")
            await UserStates.GET_FULLNAME.set()
        else:
            books = await bks.get_books()
            if not books:
                await message.answer(text="Hozircha testlar mavjud emas!")
            else:
                await message.answer(text="Javoblarni yuborish uchun testni tanlang",
                                     reply_markup=user_main_ikb(books=books))
    else:
        await message.answer(text="Siz foydalanuvchilar ro'yxatida yo'q ekansiz! /start buyrug'ini kiritib botni "
                                  "qayta ishga tushiring!")


@dp.message_handler(state=UserStates.GET_FULLNAME, content_types=types.ContentType.TEXT)
async def handle_get_fullname(message: types.Message, state: FSMContext):
    if message.text.isascii():
        data = await state.get_data()
        user_id = data.get('student_user_id')
        full_name = message.text
        await udb.set_full_name(full_name=full_name, user_id=user_id)
        books = await bks.get_books()
        if not books:
            await message.answer(text="Hozircha testlar mavjud emas!")
        else:
            await message.answer(text="Javoblarni yuborish uchun testni tanlang",
                                 reply_markup=user_main_ikb(books=books))
    else:
        await message.answer(text="Namunadagidek kiritilishi lozim!")


@dp.callback_query_handler(F.data.startswith("user_test:"), state="*")
async def handle_user_test(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=0)
    book_id = int(call.data.split(":")[1])
    await state.update_data(student_book_id=book_id)
    book = await bks.get_book_name_file_id(book_id=book_id)

    await call.message.answer_document(document=book['file_id'],
                                       caption=f"Test nomi: {book['name']}\n\n"
                                               f"Javoblarni kiriting\n\n(javoblar faqat lotin harflarida kiritilishi "
                                               f"lozim! katta kichikligini ahamiyati yo'q):\n\n"
                                               f"<b>Namuna: abcdabcdabcd</b>")
    await UserStates.GET_ANSWERS.set()


@dp.message_handler(state=UserStates.GET_ANSWERS, content_types=types.ContentType.TEXT)
async def handle_user_answers(message: types.Message, state: FSMContext):
    data = await state.get_data()
    book_id = data.get('student_book_id')
    user_id = data.get('student_user_id')

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

    # for i, (user_answer, correct_answer) in enumerate(zip(user_answers, correct_answers), 1):
    #
    #     if user_answer == correct_answer[0]:
    #         correct_count += 1
    #         result_details += f"{i}. {user_answer.upper()}  ✅   "
    #     else:
    #         incorrect_count += 1
    #         result_details += f"{i}. {user_answer.upper()}  ❌ | ({correct_answer[0].upper()})  ✅    "
    #     if i % 2 == 0:
    #         result_details += "\n\n"

    # Ikkita ustunli formatda tahlil tuzish
    lines = []
    half = (len(correct_answers) + 1) // 2  # Agar toq bo‘lsa, chap ustun uzunroq bo‘ladi

    for i in range(half):
        left_index = i
        right_index = i + half

        # Chap ustun
        user_answer_left = user_answers[left_index]
        correct_left = correct_answers[left_index][0]
        if user_answer_left == correct_left:
            left_result = f"{left_index + 1}. {user_answer_left.upper()} ✅"
        else:
            left_result = f"{left_index + 1}. {user_answer_left.upper()} ❌ | ({correct_left.upper()}) ✅"

        # O‘ng ustun (agar mavjud bo‘lsa)
        if right_index < len(correct_answers):
            user_answer_right = user_answers[right_index]
            correct_right = correct_answers[right_index][0]
            if user_answer_right == correct_right:
                right_result = f"{right_index + 1}. {user_answer_right.upper()} ✅"
            else:
                right_result = f"{right_index + 1}. {user_answer_right.upper()} ❌ | ({correct_right.upper()}) ✅"
            line = f"{left_result:<20} {right_result}"
        else:
            line = left_result  # Faqat chap ustun

        lines.append(line)

    result_details = "\n\n".join(lines)
    await stdb.set_student_point(correct=correct_count, incorrect=incorrect_count, book_id=book_id, user_id=user_id)
    all_points = await stdb.sum_points(user_id=user_id)

    # Natijani xabar qilish
    await message.answer(
        text=f"<b>{message.from_user.full_name}</b> Siz bergan javoblar qabul qilindi.\n\nNatijangiz quyidagicha:\n\n"
             f"To'g'ri javoblar: {correct_count} ta\n"
             f"Noto'g'ri javoblar: {incorrect_count} ta\n\n"
             f"Javoblar tahlili:\n\n{result_details}\n\n"
             f"Jami to'plagan ballingiz: {all_points}"
    )
    await state.finish()
