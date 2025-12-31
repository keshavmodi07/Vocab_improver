import sqlite3
DB_name="words.db"
def get_db():
    return sqlite3.connect(DB_name)
def init_db():
    with get_db()as conn:
        cur=conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS words(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     word TEXT UNIQUE,
                     definition TEXT,
                     weight INTEGER DEFAULT 0,
                     times_asked INTEGER DEFAULT 0,
                     times_correct INTEGER DEFAULT 0)""")
        
        conn.commit()
        cur.close()
def login():
    with get_db() as conn:
        cur=conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)""")
        conn.commit()
        cur.close()
def reset_db():
    with get_db() as conn:
        conn.execute("DROP TABLE IF EXISTS words")
        conn.commit()
    init_db()
