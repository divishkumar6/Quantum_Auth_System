import sqlite3
from pathlib import Path

DB_NAME = Path(__file__).resolve().parent / "users.db"
EXPECTED_COLUMNS = ["username", "name", "email", "phone", "public_key"]


def _get_user_columns(cursor):
    cursor.execute("PRAGMA table_info(users)")
    return [row[1] for row in cursor.fetchall()]


def _migrate_users_table(cursor):
    cursor.execute("ALTER TABLE users RENAME TO users_legacy")
    cursor.execute("""
    CREATE TABLE users (
        username TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        public_key TEXT NOT NULL
    )
    """)
    cursor.execute("""
    INSERT INTO users (username, name, email, phone, public_key)
    SELECT
        username,
        COALESCE(name, ''),
        '',
        '',
        ''
    FROM users_legacy
    """)
    cursor.execute("DROP TABLE users_legacy")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        public_key TEXT NOT NULL
    )
    """)

    columns = _get_user_columns(cursor)
    if columns != EXPECTED_COLUMNS:
        _migrate_users_table(cursor)

    conn.commit()
    conn.close()


def add_user(username, name, email, phone, public_key):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO users (username, name, email, phone, public_key)
        VALUES (?, ?, ?, ?, ?)
        """, (username, name, email, phone, public_key))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    conn.close()
    return user
