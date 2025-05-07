from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_main_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
admin_main_buttons.row("➕ Test qo'shish", "➖ Test o'chirish")
admin_main_buttons.row("📊 Natijalarni ko'rish")
admin_main_buttons.row("😎 Foydalanuvchilar soni")
admin_main_buttons.row("✅ Oddiy post yuborish")
admin_main_buttons.row("🎞 Mediagroup post yuborish")
admin_main_buttons.row(KeyboardButton("🏡 Bosh sahifa"))

admin_rating_dkb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_rating_dkb.row("🤗 Umumiy", "😎 Shaxsiy")
admin_rating_dkb.row("🔙 Ortga")
