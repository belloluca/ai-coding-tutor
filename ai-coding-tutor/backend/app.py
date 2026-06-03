from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()

    message = data.get("message", "")
    mode = data.get("mode", "Tutor")

    if mode == "Tutor":
        response = "Sono in modalità Tutor. Posso spiegarti l'argomento passo dopo passo."
    elif mode == "Debug codice":
        response = "Sono in modalità Debug codice. Posso aiutarti a individuare eventuali errori nel codice."
    elif mode == "Esercizi":
        response = "Sono in modalità Esercizi. Posso proporti un esercizio sull'argomento richiesto."
    elif mode == "Quiz":
        response = "Sono in modalità Quiz. Posso generare alcune domande per verificare la tua preparazione."
    else:
        response = "Modalità non riconosciuta."

    return jsonify({
        "reply": response
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)