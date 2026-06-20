import sqlite3
from datetime import datetime
from typing import Optional, Tuple

DB_NAME = "data/bot_memory.db"

ALLOWED_COLUMNS = {"favorite_drink", "last_mood"}


def init_db() -> None:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                favorite_drink TEXT,
                last_mood TEXT,
                level INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0,
                is_banned INTEGER DEFAULT 0,
                created_at TEXT,
                last_seen TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_stats (
                user_id INTEGER,
                stat_key TEXT,
                stat_value INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, stat_key),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        conn.commit()


def get_user(user_id: int) -> Optional[Tuple]:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT first_name, favorite_drink, last_mood, level, xp, is_banned "
            "FROM users WHERE user_id = ?",
            (user_id,),
        )
        return cursor.fetchone()


def save_user(user_id: int, first_name: str) -> None:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
        exists = cursor.fetchone()
        now = datetime.now().isoformat()
        if not exists:
            cursor.execute(
                "INSERT INTO users (user_id, first_name, created_at, last_seen) "
                "VALUES (?, ?, ?, ?)",
                (user_id, first_name, now, now),
            )
        else:
            cursor.execute(
                "UPDATE users SET first_name = ?, last_seen = ? WHERE user_id = ?",
                (first_name, now, user_id),
            )
        conn.commit()


def update_user_param(user_id: int, param: str, value: str) -> None:
    if param not in ALLOWED_COLUMNS:
        return
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE users SET {param} = ?, last_seen = ? WHERE user_id = ?",
            (value, datetime.now().isoformat(), user_id),
        )
        conn.commit()


def add_xp(user_id: int, amount: int = 10) -> Optional[int]:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT xp, level FROM users WHERE user_id = ?",
            (user_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        xp, level = row
        xp += amount
        new_level = level
        while xp >= level * 100:
            xp -= level * 100
            new_level += 1
        cursor.execute(
            "UPDATE users SET xp = ?, level = ?, last_seen = ? WHERE user_id = ?",
            (xp, new_level, datetime.now().isoformat(), user_id),
        )
        conn.commit()
        if new_level > level:
            return new_level
        return None


def increment_stat(user_id: int, stat_key: str) -> None:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_stats (user_id, stat_key, stat_value) VALUES (?, ?, 1) "
            "ON CONFLICT(user_id, stat_key) DO UPDATE SET stat_value = stat_value + 1",
            (user_id, stat_key),
        )
        conn.commit()


def get_stats(user_id: int) -> dict:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT stat_key, stat_value FROM user_stats WHERE user_id = ?",
            (user_id,),
        )
        rows = cursor.fetchall()
        return dict(rows) if rows else {}


def get_all_users() -> list:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, first_name FROM users WHERE is_banned = 0")
        return cursor.fetchall()


def set_ban(user_id: int, banned: bool = True) -> None:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET is_banned = ? WHERE user_id = ?",
            (1 if banned else 0, user_id),
        )
        conn.commit()


def is_banned(user_id: int) -> bool:
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT is_banned FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        return bool(row[0]) if row else False
