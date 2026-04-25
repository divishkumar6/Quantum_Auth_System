import sqlite3
from pathlib import Path


DB_NAME = Path(__file__).resolve().parent / "users.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            public_key TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def add_user(username, name, email, phone, public_key):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, name, email, phone, public_key)
            VALUES (?, ?, ?, ?, ?)
            """,
            (username, name, email, phone, public_key),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, name, email, phone, public_key FROM users WHERE username = ?",
        (username,),
    )
    user = cursor.fetchone()
    conn.close()
    return user
