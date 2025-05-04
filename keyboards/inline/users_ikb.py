from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def user_main_ikb(books):
    btn = InlineKeyboardMarkup(row_width=1)
    for book in books:
        btn.insert(InlineKeyboardButton(text=book['name'], callback_data=f"user_test:{book['book_id']}"))
    return btn
