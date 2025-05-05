from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from data.config import ADMINS
from keyboards.inline.users_ikb import user_main_ikb
from loader import dp, bot, bks, udb


async def send_welcome_message(message: types.Message):
    CHANNEL = None
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
    await udb.add_user(telegram_id=message.from_user.id)
    await bot.send_message(chat_id=ADMINS[0],
                           text=f"{message.from_user.full_name} | <code>{message.from_user.id}</code>")
    books = await bks.get_books()
    await message.answer(
        text=f"Assalomu alaykum, {message.from_user.full_name}!\n\nKanalga majburiy obuna kerak bo'lsa yoki boshqa har "
             f"qanday funksiyalar kerak bo'lsa qo'shib beramiz! Bemalol murojaat qilavering!\n\n"
             f"Admin panelni ishlatish uchun /admin buyrug'ini kiriting\n\n")
    if not books:
        await message.answer(text="Hozircha testlar mavjud emas!")
    else:
        await message.answer(text="Javoblarni yuborish uchun testni tanlang",
                             reply_markup=user_main_ikb(books=books))

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
