import sqlite3

DB_NAME = "storage/users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        name TEXT,
        gender TEXT,
        mobile TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_user(username, name, gender, mobile):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO users (username, name, gender, mobile)
        VALUES (?, ?, ?, ?)
        """, (username, name, gender, mobile))
        conn.commit()
        return True
    except:
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