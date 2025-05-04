from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from keyboards.inline.admin_ikb import admin_del_tests
from loader import dp, bks


@dp.message_handler(IsBotAdminFilter(), F.text == "Test o'chirish", state="*")
async def handle_del_test(message: types.Message, state: FSMContext):
    await state.finish()
    tests = await bks.get_books()
    if not tests:
        await message.answer(text="Hozircha bazada testlar to'plami mavjud emas!")
    else:
        await message.answer(text="O'chirilishi kerak bo'lgan testlar to'plamini tanlang",
                             reply_markup=admin_del_tests(tests=tests))


@dp.callback_query_handler(F.data.startswith("del_test:"))
async def handle_del_test_ck(call: types.CallbackQuery):
    book_id = int(call.data.split(":")[1])

    await bks.delete_book(book_id=book_id)
    tests = await bks.get_books()
    try:
        if not tests:
            await call.message.edit_text(text="Barcha test to'plamlari o'chirildi!")
        else:
            await call.message.edit_text(text="O'chirilishi kerak bo'lgan testlar to'plamini tanlang",
                                         reply_markup=admin_del_tests(tests=tests))
    except ValueError:
        print("sasa")
