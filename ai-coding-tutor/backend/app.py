from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()

    message = data.get("message", "")
    mode = data.get("mode", "tutor")

    response = f"Studente: {message}. Modalità selezionata: {mode}"

    return jsonify({
        "response" : response
    })

    if __name__ == "__main__":
        app.run(debug = True, port = 5000)
