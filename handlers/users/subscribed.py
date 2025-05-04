from aiogram import types
from aiogram.utils.deep_linking import get_start_link
from magic_filter import F

from data.config import CHANNEL
from loader import bot, dp


async def invite_link_(user_id):
    link = await get_start_link(user_id)
    text = (
        f"\n\n📚 Qiymati 2000$ bo'lgan Milliy Sertifikat kitobini olish uchun quyidagi havola orqali botga a'zo "
        f"bo'ling:\n\n{link}")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Yuborish", switch_inline_query=text))
    return markup


@dp.callback_query_handler(F.data == "subscribed")
async def subscribe_callback(call: types.CallbackQuery):
    CHANNEL = None
    status = (await bot.get_chat_member(chat_id=CHANNEL, user_id=call.from_user.id)).status

    if status == 'left' or status == 'kick':
        await call.answer(
            text="Siz kanalimizga a'zo bo'lmagansiz!", show_alert=True
        )
    else:
        await call.message.edit_text(text=f"So'nggi qadam!\n\nKitobimizni qo'lga kiritish uchun Kimyo-Biologiya "
                                          f"o'qiydigan 5 ta do'stingizni taklif qiling.\n\n"
                                          f"Kitobni yopiq kanalga joyladik takliflar soni 5 ta bo'lganda Siz ushbu "
                                          f"kanalga havola(link) olasiz.",
                                     reply_markup=await invite_link_(call.from_user.id))
