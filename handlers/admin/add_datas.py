from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from loader import dp, udb, bks
from services.batch import process_users_in_batches
from services.books import book_datas
from services.users_json import users_dict


@dp.message_handler(IsBotAdminFilter(), F.text == "add_users", state="*")
async def handle_add_users(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="User qo'shish boshlandi!")
    await process_users_in_batches(users=users_dict, db=udb)
    await message.answer(text="User qo'shish tugadi!")


@dp.message_handler(IsBotAdminFilter(), F.text == "add_books", state="*")
async def handle_add_books(message: types.Message, state: FSMContext):
    await state.finish()
    for value in book_datas:
        await bks.add_question()