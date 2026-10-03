from app.bot.instance import ptb_app
from app.bot.handlers import get_handlers
# from app.bot.middlewares.db import register_db_middleware


def setup_bot() -> None:
    # register_db_middleware(ptb_app)
    for handler in get_handlers():
        ptb_app.add_handler(handler)
