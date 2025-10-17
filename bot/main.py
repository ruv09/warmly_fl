import asyncio
import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("warmly-bot")

# Reduce noisy HTTP logs that may leak bot token in URLs
for noisy_logger_name in ("httpx", "httpcore"):
    logging.getLogger(noisy_logger_name).setLevel(logging.WARNING)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_first = update.effective_user.first_name if update.effective_user else "друг"
    await update.message.reply_text(
        f"Привет, {user_first}! Я — Warmly Bot. Напиши мне — я отвечу тёплым эхом."
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Доступные команды:\n/start — приветствие\n/help — помощь")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    text = update.message.text or ""
    if not text.strip():
        return
    await update.message.reply_text(f"Тёплое эхо: {text}")


def build_application(token: str) -> Application:
    app = (
        Application.builder()
        .token(token)
        .concurrent_updates(True)
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    return app


async def main() -> None:
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    if not token:
        logger.error("BOT_TOKEN не найден. Убедитесь, что он задан в .env")
        raise SystemExit(1)

    app = build_application(token)
    logger.info("Запуск бота (long polling)…")
    await app.initialize()
    try:
        await app.start()
        await app.updater.start_polling(drop_pending_updates=True)
        logger.info("Бот запущен и слушает обновления")
        # Ожидаем сигнала завершения
        await asyncio.Event().wait()
    finally:
        logger.info("Остановка бота…")
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Завершение по Ctrl+C")
