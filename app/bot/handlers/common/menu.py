from telegram import Update
from telegram.ext import ContextTypes


async def cb_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # stop the loading spinner

    data = query.data

    if data == "menu:profile":
        user = query.from_user
        await query.edit_message_text(
            f"🆔 ID: <code>{user.id}</code>\n"
            f"👤 Name: {user.full_name}\n"
            f"🔗 Username: @{user.username or '—'}",
            parse_mode="HTML",
        )
    elif data == "menu:help":
        await query.edit_message_text(
            "This bot demonstrates async FastAPI + PTB + Redis persistence."
        )
    elif data == "menu:register":
        await query.edit_message_text("📝 Registration flow coming soon.")
    else:
        await query.edit_message_text("Unknown action.")
