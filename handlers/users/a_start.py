from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from keyboards.default.users_dkb import user_main_dkb
from loader import dp, udb


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    await udb.add_user(telegram_id=message.from_user.id)

    await message.answer(text=f"👋 Assalomu alaykum, <b>{message.from_user.full_name}</b>!\n\n"
                              "🎉 Botimizga xush kelibsiz!", reply_markup=user_main_dkb)

#
# @dp.message_handler(IsBotAdminFilter(), F.text == "add_users")
# async def add_users_to_database(message: types.Message):
#     count = 0
#     for index, user in enumerate(users_list):
#         count += index
#         if index % 100 == 0:
#             await asyncio.sleep(2)
#         await db.add_user(telegram_id=user)
#     await message.answer(
#         text=f"Jami: {count}"
#     )
