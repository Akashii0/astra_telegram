from typing import Any

from telegram import Update
from telegram.ext import Application, ContextTypes, TypeHandler

from app.core.database import AsyncSessionLocal


async def inject_db_session(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Runs before every update handler; attaches an AsyncSession to context."""
    session = AsyncSessionLocal()
    context.user_data["_db_session"] = session


async def cleanup_db_session(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Runs after every update handler; commits or rolls back."""
    session = context.user_data.pop("_db_session", None)
    if session is None:
        return
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


def register_db_middleware(application: Application) -> None:
    # Priority: lower = earlier. These run for every update.
    application.add_handler(TypeHandler(Update, inject_db_session), group=-10)
    application.add_handler(TypeHandler(Update, cleanup_db_session), group=10)
