from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminStates(StatesGroup):
    SEND_MEDIA_TO_USERS = State()
    SEND_TO_USERS = State()
    ADD_BOOK = State()
    ADD_BOOK_PDF = State()
    ADD_TEXT_KEYS = State()
    GET_FULL_NAME = State()
    DEL_USER = State()
    RENAME_BOOKS = State()
