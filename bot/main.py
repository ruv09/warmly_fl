from __future__ import annotations
import asyncio
import logging

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
)

from .config import require_token, DB_PATH
from .storage import init_db
from .handlers import (
    cmd_start,
    cmd_help,
    cmd_mood,
    on_mood_choice,
    on_save,
    on_another,
    cmd_archive,
    cmd_send,
    on_friend_another,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("warmly.bot")


async def _bootstrap() -> None:
    token = require_token()

    # init database
    await init_db(DB_PATH)

    app = Application.builder().token(token).build()

    # pass db path into app context
    app.bot_data["db_path"] = DB_PATH

    # commands
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("mood", cmd_mood))
    app.add_handler(CommandHandler("archive", cmd_archive))
    app.add_handler(CommandHandler("send", cmd_send))

    # callbacks
    app.add_handler(CallbackQueryHandler(on_mood_choice, pattern=r"^mood:(good|ok|bad)$"))
    app.add_handler(CallbackQueryHandler(on_another, pattern=r"^another:(good|ok|bad)$"))
    app.add_handler(CallbackQueryHandler(on_friend_another, pattern=r"^friend:another$"))
    app.add_handler(CallbackQueryHandler(on_save, pattern=r"^save$") )

    logger.info("Bot is starting...")
    await app.initialize()
    await app.start()
    try:
        await app.updater.start_polling(drop_pending_updates=True)
        logger.info("Bot is running. Press Ctrl+C to stop.")
        await asyncio.Event().wait()  # run forever
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(_bootstrap())
    except KeyboardInterrupt:
        pass
