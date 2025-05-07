import aiogram.utils.exceptions

from keyboards.inline.admin_ikb import admin_del_tests
from loader import bks


async def show_delete_tests_menu(message_obj, is_edit=False):
    """Testlar ro'yxatini ko'rsatadi yoki barcha testlar o'chirilgani haqida xabar beradi"""
    try:
        tests = await bks.get_books()

        if not tests:
            text = "Hozircha bazada testlar to'plami mavjud emas!"
            if is_edit:
                text = "Barcha test to'plamlari o'chirildi!"
        else:
            text = "O'chirilishi kerak bo'lgan testlar to'plamini tanlang"

        if is_edit:
            await message_obj.edit_text(text=text, reply_markup=admin_del_tests(tests=tests) if tests else None)
        else:
            await message_obj.answer(text=text, reply_markup=admin_del_tests(tests=tests) if tests else None)
    except aiogram.utils.exceptions.BadRequest:
        await message_obj.answer(text="Savollar kitoblari mavjud emas!")
