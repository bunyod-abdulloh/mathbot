from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from filters.admins import IsBotAdminFilter
from loader import dp, udb
from services.batch import process_users_in_batches
from services.users_json import users_dict


@dp.message_handler(IsBotAdminFilter(), F.text == "add_users", state="*")
async def handle_add_users(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="User qo'shish boshlandi!")
    await process_users_in_batches(users=users_dict, db=udb)
    await message.answer(text="User qo'shish tugadi!")
