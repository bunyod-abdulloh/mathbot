from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.users_ikb import user_main_ikb
from loader import dp, bks, udb, stdb
from states.users import UserStates


@dp.message_handler(F.text == "✅ Javoblarni kiritish", state="*")
async def handle_user_main(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = await udb.select_user(telegram_id=message.from_user.id)

    await state.update_data(student_user_id=user_id)
    if user_id:
        check_student = await stdb.check_student(user_id=user_id)
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
        print(books)
        if not books:
            await message.answer(text="Hozircha testlar mavjud emas!")
        else:
            await message.answer(text="Javoblarni yuborish uchun testni tanlang",
                                 reply_markup=user_main_ikb(books=books))
        await stdb.add_student(user_id=user_id)
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

    # Ikkita ustunli formatda tahlil tuzish - monospace formatda aniqroq ustunlash
    lines = []
    half = (len(correct_answers) + 1) // 2

    correct_count = 0
    incorrect_count = 0

    # Chap va o‘ng ustunlarni alohida shakllantirish
    left_column = []
    right_column = []
    in_correct = []

    # Chap ustun
    for i in range(half):
        user_answer = user_answers[i]
        correct = correct_answers[i][0]
        if user_answer == correct:
            result = f"{i + 1:02d}. {user_answer.upper()} ✅"
            correct_count += 1
        else:
            result = f"{i + 1:02d}. {user_answer.upper()} ❌"
            in_correct.append(f"{i + 1:02d}. {user_answer.upper()} ❌ | To'g'ri javob {correct.upper()} ✅")
            incorrect_count += 1
        left_column.append(result)

    # O‘ng ustun
    for i in range(half, len(correct_answers)):
        user_answer = user_answers[i]
        correct = correct_answers[i][0]
        if user_answer == correct:
            result = f"{i + 1:02d}. {user_answer.upper()} ✅"
            correct_count += 1
        else:
            result = f"{i + 1:02d}. {user_answer.upper()} ❌"
            in_correct.append(f"{i + 1:02d}. {user_answer.upper()} ❌ | To'g'ri javob {correct.upper()} ✅")
            incorrect_count += 1
        right_column.append(result)

    # Natijalar jadvalini shakllantirish - monospace shrift uchun
    max_left_length = max(len(item) for item in left_column) + 20

    # Jadvalni shakllantirish
    for i in range(len(left_column)):
        left_item = left_column[i]
        right_item = right_column[i] if i < len(right_column) else ""
        line = f"{left_item}{' ' * (max_left_length - len(left_item))}{right_item}"
        lines.append(line)

    # Noto'g'ri javoblarni bitta ustunda joylashtirish
    in_correct_lines = []
    for i in range(len(in_correct)):
        in_correct_lines.append(f"{in_correct[i]}")

    # Yangi formatda xabarni yuborish
    result_details = "\n\n".join(lines)
    incorrect_text = "📝 Izoh:\n <blockquote expandable>" + "\n\n".join(
        in_correct_lines) + "</blockquote>" if in_correct else ""

    check_book = await stdb.check_book_by_id(book_id=book_id, user_id=user_id)

    if check_book:
        await stdb.set_student_point(correct=correct_count, incorrect=incorrect_count, book_id=book_id, user_id=user_id)
    else:
        await stdb.add_student_datas(user_id=user_id, book_id=book_id, correct=correct_count, incorrect=incorrect_count)
    all_points = await stdb.sum_points(user_id=user_id)
    full_name = await udb.get_full_name(user_id=user_id)
    text = str()

    if in_correct:
        text += f"{incorrect_text}\n\n"

    await message.answer(
        text=f"👤 <b>{full_name}</b>\n📩 Javoblaringiz qabul qilindi.\n\n"
             f"📊 Natijangiz::\n\n"
             f"✅ To‘g‘ri javoblar: {correct_count} ta\n"
             f"❌ Noto‘g‘ri javoblar: {incorrect_count} ta\n"
             f"🎯 Jami ball: {all_points}\n\n"
             f"📋 Javoblar:\n <blockquote>{result_details}</blockquote>\n\n"
             f"{text}",
        parse_mode="HTML"
    )
    await state.finish()
