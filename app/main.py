# Lifespan (startup, shutdown)
import asyncio
from contextlib import asynccontextmanager

from anyio import to_thread
from fastapi import Depends, FastAPI, HTTPException, Header, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy.orm import Session
from telegram import Update

from app.bot.instance import ptb_app
from app.bot.setup import setup_bot

# from app.core.database import get_session
from app.core.settings import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """This is the startup and shutdown code for the FastAPI application."""
    # Startup code
    print("Starting Server...")

    # Bigger Threadpool i.e you send a bunch of requests it will handle a max of 1000 at a time, the default is 40 # pylint: disable=line-too-long
    limiter = to_thread.current_default_thread_limiter()
    limiter.total_tokens = 1000

    # ---- PTB startup ----
    setup_bot()
    await ptb_app.initialize()
    await ptb_app.start()
    await ptb_app.bot.set_webhook(
        url=f"{settings.WEBHOOK_BASE_URL}/webhook/telegram",
        secret_token=settings.WEBHOOK_SECRET,
        allowed_updates=Update.ALL_TYPES,
    )

    # Shutdown Code
    yield

    # ---- PTB shutdown (graceful) ----
    # 1. Stop accepting new updates by deleting the webhook
    await ptb_app.bot.delete_webhook()
    print("Webhook deleted. No new updates will be sent.")

    # 2. Give in-flight updates time to be processed by PTB's internal queue.
    #    The `stop` method waits for the update processor to finish.
    print("Stopping bot application and waiting for in-flight updates...")
    await ptb_app.stop()

    # 3. Shut down the bot's session and resources
    await ptb_app.shutdown()
    print("Bot application shut down cleanly.")

    print("Shutting Down Server...")

app = FastAPI(
    title="Astra Bot",
    lifespan=lifespan,
    # default_response_class=ORJSONResponse,
    docs_url="/",
    contact={
        "name": "Ayria Technologies",
        "url": "https://github.com/AyriaTechnologies",
        "email": "ayriatechnologies@gmail.com",
    },
)

# Allowed Origins
origins = ["*"]

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    GZipMiddleware,
    minimum_size=5000,  # Minimum size of the response before it is compressed in bytes
)


# # Healthcheck
# @app.get("/health")
# async def health(_: Session = Depends(get_session)):
#     """App Healthcheck"""
#     return {"status": "Ok!"}
# Healthcheck
@app.get("/health")
async def health():
    """App Healthcheck"""
    return {"status": "Ok!"}


@app.post("/webhook/telegram", include_in_schema=False)
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str = Header(None),
):
    # Verify the request actually came from Telegram
    if x_telegram_bot_api_secret_token != settings.WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret token")

    data = await request.json()
    print(data)
    try:
        update = Update.de_json(data, ptb_app.bot)
        if update:
            # Enqueue the update for PTB's internal processor
            await ptb_app.update_queue.put(update)
    except Exception as e:
        # Log the exception but always return a 200 to prevent Telegram from retrying a poison-pill update
        print(f"Error processing update: {e}")
        return Response(status_code=200)

    # Return 200 OK immediately, signaling to Telegram that the update was received.
    return Response(status_code=200)


@app.get("/ping")
async def ping():
    return {"pong": True}
