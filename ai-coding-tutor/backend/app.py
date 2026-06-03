from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    mode = data.get('mode', 'Tutor')

    if mode == 'Tutor':
        response = f""" 
        Modalità Tutor.

        Ti spiego il seguente argomento:
            {message}

        Spiegazione

        """
    elif mode == 'Quiz':
        response = f""" 

        Modalità Quiz.

        In base alla richiesta:
            {message}

        Esercizio:
            A)
            B)
            C)
            D)

        """
    elif mode == 'Debug codice':
        response = f"""

        Modalita di Debug del codice.

        Codice inserito o richiesta:
            {message}

        Suggerimenti:
            ....
            ....
    
        """

    elif mode == 'Esercizi':
        response = f""" 

        Modalità Esercizi.

        In base alla richiesta:
            {message}

        Esercizio:
            Svolgi la somma

        """
    else:
        response = "Modalità non riconosciuta"

    return jsonify({
        "response": response
    })

if __name__ == '__main__':
    app.run(debug=True)