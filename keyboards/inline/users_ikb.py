from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def user_main_ikb(books):
    btn = InlineKeyboardMarkup(row_width=1)
    for book in books:
        btn.insert(InlineKeyboardButton(text=book['name'], callback_data=f"user_test:{book['book_id']}"))
    return btn


def key_returner(current_page, all_pages):
    keys = InlineKeyboardMarkup(row_width=3)
    keys.row(
        InlineKeyboardButton(
            text="◀️",
            callback_data=f"prev_all:{current_page}"
        ),
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data=f"alertall:{current_page}"
        ),
        InlineKeyboardButton(
            text="▶️",
            callback_data=f"next_all:{current_page}"
        )
    )
    return keys
