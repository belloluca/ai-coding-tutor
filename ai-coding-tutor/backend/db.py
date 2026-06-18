import sqlite3

# Connessione al database SQLite
conn = sqlite3.connect("database.db")

# Creazione del cursore per eseguire query SQL
cursor = conn.cursor()

# Creazione della tabella dedicata agli utenti
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

# Creazione della tabella dedicata alle chat degli utenti
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

# Salva definitivamente le modifiche nel database
conn.commit()

# Chiude la connessione al database
conn.close()

print("Database inizializzato correttamente.")