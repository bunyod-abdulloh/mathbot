from aiogram.types import ReplyKeyboardMarkup

user_main_dkb = ReplyKeyboardMarkup(resize_keyboard=True)
user_main_dkb.row("📊 Natijalar", "✅ Javoblarni kiritish")

results_dkb = ReplyKeyboardMarkup(resize_keyboard=True)
results_dkb.row("🤗 Umumiy", "😎 Shaxsiy")
results_dkb.row("🔙 Ortga")
