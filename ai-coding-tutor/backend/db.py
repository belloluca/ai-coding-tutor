import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,

    -- 0 = email non verificata
    -- 1 = email verificata
    email_verificata INTEGER NOT NULL DEFAULT 0,

    -- Token univoco utilizzato per confermare l'indirizzo email
    token_conferma TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    modalita TEXT NOT NULL,
    messaggio_utente TEXT NOT NULL,
    risposta_ai TEXT NOT NULL,
    creato_il TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

conn.commit()

conn.close()

print("Database inizializzato correttamente.")