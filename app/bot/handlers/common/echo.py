from telegram import Update
from telegram.ext import ContextTypes


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply to any plain text message."""
    await update.message.reply_text(f"📩 You said: {update.message.text}")


async def echo_no_quote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply WITHOUT quoting the user's message."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"📩 (no quote) {update.message.text}",
    )


async def echo_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle photos, voice, documents, etc."""
    msg = update.message
    if msg.photo:
        await msg.reply_text("📷 Nice photo!")
    elif msg.voice:
        await msg.reply_text("🎤 Got your voice note!")
    elif msg.document:
        await msg.reply_text(f"📄 File: {msg.document.file_name}")
    elif msg.sticker:
        await msg.reply_text(f"🎨 Sticker: {msg.sticker.emoji}")
