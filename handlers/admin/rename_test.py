from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from keyboards.inline.admin_ikb import rename_books_ikb
from loader import dp, bks
from services.functions import no_test_text, answer_text
from states.admin import AdminStates


@dp.message_handler(IsBotAdminFilter(), F.text == "📗 Test nomini o'zgartirish", state="*")
async def handle_rename_test(message: types.Message, state: FSMContext):
    await state.finish()
    books = await bks.get_books()
    if not books:
        await message.answer(text=no_test_text)
    else:
        await message.answer(text=answer_text, reply_markup=rename_books_ikb(books=books))


@dp.callback_query_handler(F.data.startswith("rename_books:"), state="*")
async def handle_rename_test_call(call: types.CallbackQuery, state: FSMContext):
    book_id = int(call.data.split(":")[1])
    await state.update_data(rename_book=book_id)
    await call.message.edit_text(text="📝 Yangi nom kiriting")
    await AdminStates.RENAME_BOOKS.set()


@dp.message_handler(state=AdminStates.RENAME_BOOKS, content_types=types.ContentType.TEXT)
async def handle_rename_test_st(message: types.Message, state: FSMContext):
    book_id = (await state.get_data()).get('rename_book')
    await bks.set_book_name(book_name=message.text, book_id=book_id)
    await message.answer(text="✅ Test nomi o'zgartirildi!")
    await state.finish()
