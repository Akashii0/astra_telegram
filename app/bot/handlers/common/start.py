from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler

from app.bot.keyboards.inline import main_menu_kb


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hey <b>{user.full_name}</b>!\n"
        f"Welcome to <b>Astra Bot</b> (Akashi RULES lol). Pick an option below:",
        reply_markup=main_menu_kb(),
        parse_mode="HTML",
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Commands:\n/start — main menu\n/help — this message\n/cancel — abort any flow"
    )


async def cmd_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # PTB conversations are cleared differently; see ConversationHandler docs
    await update.message.reply_text("❌ Cancelled.", reply_markup=main_menu_kb())
    # await update.message.reply_text("❌ Cancelled.")
