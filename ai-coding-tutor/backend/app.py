from flask import Flask, jsonify, request 
from flask_cors import CORS 
from google import genai 
from dotenv import load_dotenv 
import os 
import sqlite3 
from werkzeug.security import generate_password_hash 
from werkzeug.security import check_password_hash 
import secrets 
import smtplib 
from email.mime.text import MIMEText 

load_dotenv() 

app = Flask(__name__) 
CORS(app) 

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY")) 


@app.route('/api/chat', methods=['POST']) 
def chat():

    data = request.get_json() 

    message = data.get('message', '')
    mode = data.get('mode', 'Tutor')
    user_id = data.get("user_id", '')

    if mode == 'Tutor':
        system_prompt = """
            Sei un AI Coding Tutor per studenti universitari.

            Devi rispondere SOLO alla domanda dello studente.
            La risposta deve essere breve, semplice e inerente alla programmazione.

            Regole obbligatorie:
            - massimo 8 righe;
            - non scrivere introduzioni lunghe;
            - non parlare di argomenti non richiesti;
            - se viene chiesto un concetto, dai definizione + piccolo esempio;
            - usa un linguaggio semplice;
            - non aggiungere sezioni inutili;
            - rispondi in italiano.

            Formato:
            Definizione breve.
            Esempio di codice, se utile.
            Spiegazione finale di 1-2 frasi.
        """

    elif mode == 'Debug codice':
        system_prompt = """
        Sei un assistente per il debugging del codice.

        Devi analizzare SOLO il codice o l'errore inserito dallo studente.
        La risposta deve essere breve, pratica e utile.

        Regole obbligatorie:
        - massimo 10 righe;
        - non riscrivere tutto il codice se non serve;
        - individua l'errore principale;
        - spiega perché è un errore;
        - proponi una correzione semplice;
        - se il codice è incompleto, dillo chiaramente;
        - non parlare di argomenti non richiesti;
        - rispondi in italiano.

        Formato:
        Errore individuato:
        Spiegazione:
        Correzione:
    """

    elif mode == 'Esercizi':
        system_prompt = """
        Sei un assistente che crea esercizi di programmazione.

        Devi proporre UN SOLO esercizio coerente con la richiesta dello studente.
        Non devi dare subito la soluzione, a meno che venga richiesta esplicitamente.

        Regole obbligatorie:
        - massimo 10 righe;
        - crea un esercizio semplice e chiaro;
        - indica il linguaggio se viene specificato;
        - indica la difficoltà;
        - spiega l'obiettivo dell'esercizio;
        - non aggiungere teoria lunga;
        - non proporre più esercizi insieme;
        - rispondi in italiano.

        Formato:
        Titolo:
        Difficoltà:
        Consegna:
        Obiettivo:
    """

    elif mode == 'Quiz':
        system_prompt = """
        Sei un assistente che crea quiz di programmazione.

        Devi creare UNA SOLA domanda a risposta multipla coerente con la richiesta dello studente.

        Regole obbligatorie:
        - massimo 10 righe;
        - una sola domanda;
        - quattro risposte: A, B, C, D;
        - una sola risposta corretta;
        - aggiungi una spiegazione breve;
        - non aggiungere teoria lunga;
        - non uscire dall'argomento richiesto;
        - rispondi in italiano.

        Formato:
        Domanda:
        A)
        B)
        C)
        D)
        Risposta corretta:
        Spiegazione:
    """

    else:
        system_prompt = """
            Sei un assistente per lo studio della programmazione.

            Rispondi in italiano, in modo breve, semplice e coerente con la richiesta.
            Non superare 8 righe.
        """

    try:

        prompt = f"""
            Modalità: {mode}

            Istruzioni da seguire:
            {system_prompt}

            Domanda dello studente:
            {message}

            Rispondi rispettando esattamente la modalità selezionata.
            Non superare il limite di righe indicato.
            Non aggiungere informazioni non richieste.
        """

        ai_response = client.models.generate_content(model = "gemini-2.5-flash-lite", contents = prompt) 
        ai_text = ai_response.text

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO chats (user_id, modalita, messaggio_utente, risposta_ai)
            VALUES (?, ?, ?, ?)
        """, (user_id, mode, message, ai_text))

        conn.commit()
        conn.close()

        return jsonify({
            "response": ai_text 
        })
    
    
    except Exception as e:

        return jsonify({

            "response": "Il servizio AI non è momentaneamente disponibile oppure la quota gratuita è stata superata. Riprovare più tardi."

        })
    

@app.route("/api/register", methods=["POST"])
def register():

   
    data = request.get_json()

    nome = data.get("nome")
    email = data.get("email")
    password = data.get("password")

    if not nome or not email or not password:
        return jsonify({"error": "Compila tutti i campi"}), 400

    password_hash = generate_password_hash(password)

    # 
    token = secrets.token_urlsafe(32)

    try:

        conn = sqlite3.connect("database.db")

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (nome, email, password, email_verificata, token_conferma)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, email, password_hash, 0, token))

        send_confirmation_email(email, token)

        conn.commit()

        conn.close()

        return jsonify({
            "message": "Registrazione quasi completata. Controlla la tua email per confermare l'account."
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email già registrata"}), 409


@app.route("/api/confirm-email/<token>", methods=["GET"])
def confirm_email(token):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM users
        WHERE token_conferma = ?
    """, (token,))

    user = cursor.fetchone()

    if user is None:
        conn.close()
        return "Token non valido o già utilizzato."

    cursor.execute("""
        UPDATE users
        SET email_verificata = 1,
            token_conferma = NULL
        WHERE token_conferma = ?
    """, (token,))

    conn.commit()
    conn.close()

    return """
        <!DOCTYPE html>
        <html lang="it">
        <head>
            <meta charset="UTF-8">
            <title>Email confermata</title>
            <style>
                * {
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }

                body {
                    font-family: Arial, Helvetica, sans-serif;
                    background: #eef3f8;
                    color: #1f2937;
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }

                .card {
                    background: white;
                    padding: 40px;
                    border-radius: 18px;
                    box-shadow: 0 8px 25px rgba(15, 23, 42, 0.12);
                    text-align: center;
                    max-width: 460px;
                    width: 90%;
                }

                .icon {
                    width: 70px;
                    height: 70px;
                    margin: 0 auto 20px;
                    border-radius: 50%;
                    background: #dcfce7;
                    color: #166534;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-size: 38px;
                    font-weight: bold;
                }

                h1 {
                    font-size: 26px;
                    margin-bottom: 12px;
                    color: #0f172a;
                }

                p {
                    color: #64748b;
                    line-height: 1.6;
                    margin-bottom: 24px;
                }

                a {
                    text-decoration: none;
                }

                button {
                    border: none;
                    padding: 13px 22px;
                    border-radius: 12px;
                    background: #2563eb;
                    color: white;
                    font-weight: bold;
                    font-size: 15px;
                    cursor: pointer;
                }

                button:hover {
                    background: #1d4ed8;
                }
            </style>
        </head>
        <body>
            <div class="card">
                <div class="icon">✓</div>
                <h1>Registrazione avvenuta con successo</h1>
                <p>
                    La tua email è stata verificata correttamente.
                    Ora puoi accedere ad AI Coding Tutor con le tue credenziali.
                </p>

            </div>
        </body>
        </html>
        """
    

@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Compila tutti i campi"}), 400


    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, email, password, email_verificata
        FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()
    conn.close()

    if user is None:
        return jsonify({"error": "Email o password non corretti"}), 401

    user_id = user[0]
    nome = user[1]
    email_db = user[2]
    password_hash = user[3]
    email_verificata = user[4]

    if email_verificata == 0:
        return jsonify({"error": "Devi confermare la tua email prima di accedere"}), 403

    if not check_password_hash(password_hash, password):
        return jsonify({"error": "Email o password non corretti"}), 401

    return jsonify({
        "message": "Login effettuato con successo",
        "user": {
            "id": user_id,
            "nome": nome,
            "email": email_db
        }
    }), 200


@app.route("/api/history/<int:user_id>", methods=["GET"])
def history(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, modalita, messaggio_utente, risposta_ai, creato_il
        FROM chats
        WHERE user_id = ?
        ORDER BY creato_il DESC
    """, (user_id,))

    chats = cursor.fetchall()
    conn.close()

    history = []

    for chat in chats:
        history.append({
            "id": chat[0],
            "modalita": chat[1],
            "messaggio_utente": chat[2],
            "risposta_ai": chat[3],
            "creato_il": chat[4]
        })

    return jsonify(history), 200

@app.route("/api/delete-chat/<int:chat_id>", methods=["DELETE"])
def delete_chat(chat_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM chats
        WHERE id = ?
    """, (chat_id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "Chat eliminata correttamente"}), 200

def send_confirmation_email(to_email, token):

    link = f"http://127.0.0.1:5000/api/confirm-email/{token}"

    subject = "Conferma registrazione AI Coding Tutor"

    body = f"""
Ciao,

grazie per esserti registrato ad AI Coding Tutor.

Clicca sul link seguente per confermare la tua email:

{link}

Se non hai richiesto questa registrazione, ignora questa email.
"""

    msg = MIMEText(body, "plain", "utf-8")

    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = to_email


    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)

if __name__ == '__main__':
    app.run(debug=True)