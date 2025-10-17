import os
from pathlib import Path
from dotenv import load_dotenv

# Load variables from a local .env file if present
load_dotenv()

# Bot token from @BotFather
TELEGRAM_BOT_TOKEN: str | None = os.environ.get("TELEGRAM_BOT_TOKEN")

# SQLite file location (defaults to bot/bot.db)
DEFAULT_DB_PATH = Path(__file__).resolve().parent / "bot.db"
DB_PATH: str = os.environ.get("DB_PATH", str(DEFAULT_DB_PATH))


def require_token() -> str:
    token = TELEGRAM_BOT_TOKEN
    if not token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is not set. Create a .env with TELEGRAM_BOT_TOKEN=..."
        )
    return token
