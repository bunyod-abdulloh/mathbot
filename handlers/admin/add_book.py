from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bks
from states.admin import AdminStates


@dp.message_handler(state=AdminStates.ADD_BOOK, content_types=types.ContentType.TEXT)
async def handle_add_test_st(message: types.Message, state: FSMContext):
    await state.finish()
    book_id = await bks.add_book(name=message.text.strip())
    await message.answer(text="Qabul qilindi!\n\nKalitlarni kiriting")
