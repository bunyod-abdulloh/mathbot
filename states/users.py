from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    GET_ANSWERS = State()
    GET_FULLNAME = State()
