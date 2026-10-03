import logging

from telegram import Update, constants
from telegram.ext import ContextTypes

from app.ai.agent import assistant_agent

logger = logging.getLogger(__name__)


async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Forward non-command text to the Pydantic AI agent and reply."""
    if not update.message or not update.message.text:
        return

    user_text = update.message.text.strip()
    if not user_text:
        return

    # Show "typing…" while the model generates
    await update.message.chat.send_action(constants.ChatAction.TYPING)

    try:
        result = await assistant_agent.run(user_text)
        reply = result.output
    except Exception as exc:
        logger.exception("Pydantic AI agent failed")
        await update.message.reply_text(
            f"⚠️ Something went wrong while generating a reply. Try again. Err: {exc}"
        )
        return

    # Telegram messages are capped at 4096 chars — split if needed
    for chunk in _split_message(reply, 4000):
        await update.message.reply_text(chunk)


def _split_message(text: str, size: int) -> list[str]:
    """Split a long reply into Telegram-safe chunks on word boundaries."""
    if len(text) <= size:
        return [text]
    chunks, current = [], ""
    for word in text.split():
        if len(current) + len(word) + 1 > size:
            chunks.append(current.rstrip())
            current = ""
        current += word + " "
    if current:
        chunks.append(current.rstrip())
    return chunks
