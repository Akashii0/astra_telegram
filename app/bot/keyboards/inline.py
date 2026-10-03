from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_kb() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("👤 Profile", callback_data="menu:profile"),
            InlineKeyboardButton("📝 Register", callback_data="menu:register"),
        ],
        [
            InlineKeyboardButton("ℹ️ Help", callback_data="menu:help"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
