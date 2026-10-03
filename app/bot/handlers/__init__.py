from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, filters

from app.bot.handlers.common import ai_chat as common_ai
from app.bot.handlers.common import echo as common_echo
from app.bot.handlers.common import menu as common_menu
from app.bot.handlers.common import start as common_start


def get_handlers() -> list:
    """Order matters: more specific handlers first."""
    return [
        # ---- Commands (must come first) ----
        CommandHandler("start", common_start.cmd_start),
        CommandHandler("help", common_start.cmd_help),
        CommandHandler("cancel", common_start.cmd_cancel),

        # ---- Callback queries (inline button clicks) ----
        CallbackQueryHandler(common_menu.cb_router),
        # add user/admin handlers here

        # ---- Content-specific handlers (before catch-all) ----
        MessageHandler(filters.PHOTO, common_echo.echo_media),
        MessageHandler(filters.VOICE, common_echo.echo_media),
        MessageHandler(filters.Document.ALL, common_echo.echo_media),
        MessageHandler(filters.Sticker.ALL, common_echo.echo_media),

        # ---- Catch-all text (must be last) ----
        # MessageHandler(filters.TEXT & ~filters.COMMAND, common_echo.echo),
        MessageHandler(filters.TEXT & ~filters.COMMAND, common_ai.ai_chat),
    ]
