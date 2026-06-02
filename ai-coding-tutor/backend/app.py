from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_service import generate_ai_response
from database import init_db, save_interaction, get_history

app = Flask(__name__)
CORS(app)

init_db()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()

    user_message = data.get('message', '').strip()
    mode = data.get('mode', 'Tutor')

    if not user_message:
        return jsonify({'error': 'Messaggio vuoto'}), 400

    ai_response = generate_ai_response(user_message, mode)
    save_interaction(user_message, ai_response, mode)

    return jsonify({
        'message': user_message,
        'mode': mode,
        'response': ai_response
    })

@app.route('/api/history', methods=['GET'])
def history():
    return jsonify(get_history())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
