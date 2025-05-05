from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from loader import dp, bks
from services.admin.book import show_delete_tests_menu


@dp.message_handler(IsBotAdminFilter(), F.text == "➖ Test o'chirish", state="*")
async def handle_del_test(message: types.Message, state: FSMContext):
    await state.finish()
    await show_delete_tests_menu(message)


@dp.callback_query_handler(F.data.startswith("del_test:"))
async def handle_del_test_cb(call: types.CallbackQuery):
    try:
        book_id = call.data.split(":")[1]
        if book_id.isdigit():
            await bks.delete_book(book_id=int(book_id))
        else:
            await bks.delete_book_not_book_id()

        await show_delete_tests_menu(call.message, is_edit=True)
    except Exception as e:
        await call.message.edit_text(f"Xatolik yuz berdi: {str(e)}")
