from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_main_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
admin_main_buttons.row("➕ Test qo'shish", "➖ Test o'chirish")
admin_main_buttons.row("📗 Test nomini o'zgartirish")
admin_main_buttons.row("🧹 Jadvalni tozalash", "😎 Foydalanuvchilar soni")
admin_main_buttons.row("👤❌ Foydalanuvchini o‘chirish")
admin_main_buttons.row("✅ Oddiy post yuborish")
admin_main_buttons.row("🎞 Mediagroup post yuborish")
admin_main_buttons.row(KeyboardButton("🏡 Bosh sahifa"))
