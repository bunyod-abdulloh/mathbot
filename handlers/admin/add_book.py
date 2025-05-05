import logging
import traceback

from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.inline.admin_ikb import admin_get_keys_ikb, admin_check_question_ikb
from loader import dp, bks
from states.admin import AdminStates


@dp.message_handler(state=AdminStates.ADD_BOOK, content_types=types.ContentType.TEXT)
async def handle_add_test_st(message: types.Message, state: FSMContext):
    await state.finish()
    try:
        book_id = await bks.add_book(name=message.text.strip())
        await message.answer(text="Qabul qilindi!\n\nSavollar kitobini pdf shaklini yuboring")
        await state.update_data(admin_book_id=int(book_id))
        await AdminStates.ADD_BOOK_PDF.set()
    except Exception as err:
        logging.info(err)


@dp.message_handler(state=AdminStates.ADD_BOOK_PDF, content_types=types.ContentType.DOCUMENT)
async def handle_get_pdf(message: types.Message, state: FSMContext):
    data = await state.get_data()
    book_id = data.get("admin_book_id")

    try:
        file_id = message.document.file_id
        await bks.add_book_file_id(book_id=book_id, file_id=file_id)
        await message.answer(text="Qabul qilindi!\n\nKalit kiritish turini tanlang",
                             reply_markup=admin_get_keys_ikb())
    except Exception as err:
        await message.answer(text=f"Xatolik: {err}")


@dp.callback_query_handler(F.data == "admin_keys_xls", state="*")
async def handle_add_keys_xls(call: types.CallbackQuery):
    await call.answer(text="Hozircha matnli kiritib turing, kerak desangiz uni ham ishlatib beramiz!",
                      show_alert=True)


@dp.callback_query_handler(F.data == "admin_keys_text", state="*")
async def handle_add_keys_text(call: types.CallbackQuery):
    await call.message.edit_text(text="Kalitlarni kiriting\n\n"
                                      "<b>Namuna: abcdabcdabcdabcd</b>")
    await AdminStates.ADD_TEXT_KEYS.set()


@dp.message_handler(state=AdminStates.ADD_TEXT_KEYS, content_types=types.ContentType.TEXT)
async def handle_add_keys_text_st(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        book_id = data.get('admin_book_id')
        book_name = await bks.get_book_name(book_id=book_id)

        answers = list(message.text)

        question_answer = str()
        for index, answer in enumerate(answers, start=1):
            if index == 1:
                await bks.update_question(question_number=index, answer=answer.lower(), book_id=book_id)
            else:
                await bks.add_question(book_id=book_id, book_name=book_name, question_number=index,
                                       answer=answer.lower())
            question_answer += f" {index}. {answer.upper()}  "
            if index % 4 == 0:
                question_answer += "\n\n"

        await message.answer(text=f"{question_answer}To'plam nomi: {book_name}\n\n"
                                  f"Jami savollar soni: {len(answers)} ta\n\nTasdiqlaysizmi?",
                             reply_markup=admin_check_question_ikb(book_id=book_id))
        await state.finish()
    except Exception as err:
        logging.error(f"Xatolik: {err}")
        logging.error(traceback.format_exc())


@dp.callback_query_handler(F.data == "admin_check_yes", state="*")
async def handle_check_tests(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Tabriklaymiz, testlar muvaffaqqiyatli saqlandi!")
    await state.finish()


@dp.callback_query_handler(F.data.startswith("admin_check_reenter:"), state="*")
async def handle_reenter_tests(call: types.CallbackQuery):
    row_id = int(call.data.split(":")[1])
    await bks.delete_book_by_row_id(row_id=row_id)
    await call.message.edit_text(text="Savollar kitobi nomi yoki raqamini yuboring")
    await AdminStates.ADD_BOOK.set()
