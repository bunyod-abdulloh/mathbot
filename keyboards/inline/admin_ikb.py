from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_get_keys_ikb(book_id):
    btn = InlineKeyboardMarkup()
    btn.add(InlineKeyboardButton(text="Excel kiritish", callback_data=f"admin_keys_xls:{book_id}"))
    btn.add(InlineKeyboardButton(text="Matn kiritish", callback_data=f"admin_keys_text:{book_id}"))
    return btn


def admin_check_question_ikb(book_id):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.row(InlineKeyboardButton(text="♻️ Qayta kiritish", callback_data=f"admin_check_reenter:{book_id}"),
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"admin_check_yes"))
    return btn


def admin_del_tests(tests):
    btn = InlineKeyboardMarkup(row_width=1)
    for test in tests:
        btn.add(InlineKeyboardButton(text=test['name'], callback_data=f"del_test:{test['book_id']}"))
    return btn
