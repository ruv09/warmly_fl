from __future__ import annotations
import random
from typing import Final

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from .phrases import MOOD_GOOD, MOOD_OK, MOOD_BAD, FRIEND, random_from
from .storage import add_favorite, list_favorites


HELP_TEXT: Final[str] = (
    "Я — бот Warmly. Я присылаю тёплые слова и бережные напоминания.\n\n"
    "Доступные команды:\n"
    "/mood — выбрать настроение и получить фразу\n"
    "/send — фраза, чтобы поделиться с другом\n"
    "/archive — показать последние сохранённые фразы\n"
)


def _mood_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("😊 Хорошо", callback_data="mood:good"),
                InlineKeyboardButton("😐 Нормально", callback_data="mood:ok"),
                InlineKeyboardButton("😞 Плохо", callback_data="mood:bad"),
            ]
        ]
    )


def _phrase_keyboard(mood: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("❤️ В архив", callback_data="save"),
                InlineKeyboardButton("Ещё", callback_data=f"another:{mood}"),
            ]
        ]
    )


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я — Warmly бот. Забота начинается с малого.\n\n" + HELP_TEXT
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_TEXT)


async def cmd_mood(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Как ты себя чувствуешь?", reply_markup=_mood_keyboard())


async def on_mood_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    mood = query.data.split(":", 1)[1]
    pool = MOOD_GOOD if mood == "good" else MOOD_OK if mood == "ok" else MOOD_BAD
    phrase = random_from(pool)

    # store last phrase in user_data for quick saving
    context.user_data["last_phrase"] = phrase

    await query.edit_message_text(
        text=phrase,
        reply_markup=_phrase_keyboard(mood),
    )


async def on_another(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    mood = query.data.split(":", 1)[1]
    pool = MOOD_GOOD if mood == "good" else MOOD_OK if mood == "ok" else MOOD_BAD
    phrase = random_from(pool)
    context.user_data["last_phrase"] = phrase

    await query.edit_message_text(text=phrase, reply_markup=_phrase_keyboard(mood))


async def on_save(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer("Сохранено в архив")

    phrase = context.user_data.get("last_phrase")
    if not phrase:
        await query.edit_message_caption(caption="Не нашёл фразу для сохранения.")
        return

    user_id = update.effective_user.id
    db_path: str = context.application.bot_data["db_path"]
    await add_favorite(db_path, user_id, phrase)

    # keep message text and keyboard
    await query.edit_message_text(text=phrase, reply_markup=query.message.reply_markup)


async def cmd_archive(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    db_path: str = context.application.bot_data["db_path"]
    rows = await list_favorites(db_path, user_id, limit=10)

    if not rows:
        await update.message.reply_text(
            "Архив пуст. Получи фразу через /mood и нажми ‘В архив’."
        )
        return

    lines = ["Твои последние тёплые слова:\n"]
    for row in rows:
        when = row["created_at"].replace("T", " ")
        text = row["text"]
        lines.append(f"• {when}: {text}")

    await update.message.reply_text("\n".join(lines))


async def cmd_send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    phrase = random_from(FRIEND)
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Ещё", callback_data="friend:another")]]
    )
    await update.message.reply_text(
        f"Тёплое слово для друга:\n\n“{phrase}”", reply_markup=keyboard
    )


async def on_friend_another(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    phrase = random_from(FRIEND)
    await query.edit_message_text(
        f"Тёплое слово для друга:\n\n“{phrase}”",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Ещё", callback_data="friend:another")]]
        ),
    )
