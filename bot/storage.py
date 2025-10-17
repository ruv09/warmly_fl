from __future__ import annotations
import datetime as dt
from typing import Any
import aiosqlite


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_favorites_user_created ON favorites(user_id, created_at DESC);
"""


async def init_db(db_path: str) -> None:
    async with aiosqlite.connect(db_path) as db:
        await db.executescript(CREATE_TABLE_SQL)
        await db.commit()


async def add_favorite(db_path: str, user_id: int, text: str) -> int:
    now = dt.datetime.utcnow().isoformat()
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute(
            "INSERT INTO favorites (user_id, text, created_at) VALUES (?, ?, ?)",
            (user_id, text, now),
        )
        await db.commit()
        return cursor.lastrowid  # type: ignore[return-value]


async def list_favorites(db_path: str, user_id: int, limit: int = 10) -> list[dict[str, Any]]:
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT id, text, created_at FROM favorites WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit),
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def delete_favorite(db_path: str, user_id: int, favorite_id: int) -> int:
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute(
            "DELETE FROM favorites WHERE id = ? AND user_id = ?",
            (favorite_id, user_id),
        )
        await db.commit()
        return cursor.rowcount  # type: ignore[return-value]
