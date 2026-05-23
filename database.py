import sqlite3

DB_NAME = "bot_memory.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                favorite_drink TEXT,
                last_mood TEXT
            )
        """)
        conn.commit()

def get_user(user_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT first_name, favorite_drink, last_mood FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()

def save_user(user_id: int, first_name: str):
    if not get_user(user_id):
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (user_id, first_name) VALUES (?, ?)", (user_id, first_name))
            conn.commit()

def update_user_param(user_id: int, param: str, value: str):
    if param not in ["favorite_drink", "last_mood"]:
        return
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET {param} = ? WHERE user_id = ?", (value, user_id))
        conn.commit()
