from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from keyboards.default.users_dkb import results_dkb, user_main_dkb
from loader import dp


@dp.message_handler(F.text == "🔙 Ortga", state="*")
async def handle_back_user_main(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Bosh sahifa", reply_markup=user_main_dkb)


@dp.message_handler(F.text == "📊 Natijalar", state="*")
async def handle_rating(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text=message.text, reply_markup=results_dkb)


@dp.message_handler(F.text == "🤗 Umumiy", state="*")
async def handle_rating_all(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Bo'lim hozircha ishga tushmadi")


@dp.message_handler(F.text == "😎 Shaxsiy", state="*")
async def handle_rating_private(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Bo'lim hozircha ishga tushmadi")
