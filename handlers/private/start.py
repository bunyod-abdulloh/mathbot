import asyncio

import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from magic_filter import F

from filters.admins import IsBotAdminFilter
from utils.users_on_db import users_list
from .subscribed import invite_link_
from data.config import PRIVATE_CHANNEL, CHANNEL
from loader import dp, db, bot


async def send_welcome_message(message: types.Message):
    chat = await bot.get_chat(CHANNEL)

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(text=chat.full_name, url=f"https://t.me/{chat.username}"),
        types.InlineKeyboardButton(text="✅ A'zo bo'ldim!", callback_data="subscribed")
    )
    await message.answer(
        text="🎉 Tabriklaymiz 🎉\n\nSiz birinchi qadamni bosdingiz! Davom etish uchun yagona bo'lgan kanalimizga a'zo "
             "bo'ling.\n\nKeyin \"✅ А'zo bo'ldim!\" tugmasini bosing", reply_markup=markup)


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Salom")

@dp.message_handler(IsBotAdminFilter(), F.text == "add_users")
async def add_users_to_database(message: types.Message):
    count = 0
    for index, user in enumerate(users_list):
        count += index
        if index % 100 == 0:
            await asyncio.sleep(2)
        await db.add_user(telegram_id=user)
    await message.answer(
        text=f"Jami: {count}"
    )
