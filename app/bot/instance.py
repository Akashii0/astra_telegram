from telegram.ext import Application, ApplicationBuilder

# from app.bot.persistence.redis import RedisPersistence
from app.core.settings import get_settings

settings = get_settings()


def build_application() -> Application:
    # persistence = RedisPersistence(settings.REDIS_URL)

    return (
        ApplicationBuilder()
        .token(settings.BOT_TOKEN)
        .updater(None)  # We handle updates via FastAPI webhook
        # .persistence(persistence)
        .read_timeout(7)
        .get_updates_read_timeout(42)
        .build()
    )


ptb_app: Application = build_application()
