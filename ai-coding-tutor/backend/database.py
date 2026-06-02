import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'database' / 'chatbot.db'


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            mode TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    connection.commit()
    connection.close()


def save_interaction(question, answer, mode):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        'INSERT INTO interactions (question, answer, mode) VALUES (?, ?, ?)',
        (question, answer, mode)
    )

    connection.commit()
    connection.close()


def get_history(limit=20):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT question, answer, mode, created_at
        FROM interactions
        ORDER BY created_at DESC
        LIMIT ?
    ''', (limit,))

    rows = cursor.fetchall()
    connection.close()

    return [
        {
            'question': row[0],
            'answer': row[1],
            'mode': row[2],
            'created_at': row[3]
        }
        for row in rows
    ]
