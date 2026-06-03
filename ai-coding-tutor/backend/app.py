from flask import Flask, jsonify, request #Flask: serve per creare il server, jsonify:  per resituire oggetti JSON al front-end, request: serve per leggere i dati ricevuti dal front-end
from flask_cors import CORS #CORS: serve al frontend JavaScript di comunicare con Flask.
from openai import OpenAI #OpenAI: è il client ufficiale per chiamare l’API OpenAI.
from dotenv import load_dotenv #load_dotenv: serve per leggere variabili da un file 
import os #os: serve per leggere variabili d’ambiente del sistema.

load_dotenv() #leggo il file .env che contiene la key all'API AI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY")) #creo il client OpenAI che va a leggere la chiave dell'API dall'ambiente (contenuta in .env)

@app.route('/api/chat', methods=['POST']) #Permette di avviare la funzione sottostante quando il front-end riceve una richiesta con il metodo: POST
def chat():

    data = request.get_json() #Leggo i dati JSON ricevuti dal front-end

    #Distinguo il messaggio dalla modalità
    message = data.get('message', '')
    mode = data.get('mode', 'Tutor')

    #Verifico la modalità selezionata e mando un prompt inerente all'API AI
    if mode == 'Tutor':

        system_prompt = """
        Sei un AI Coding Tutor. Spiega gli argomenti di programmazione
        in modo semplice, chiaro e adatto a uno studente universitario.
        Usa esempi brevi quando servono.
        """

    elif mode == 'Debug codice':
        system_prompt = """
        Sei un assistente per il debugging del codice.
        Analizza il codice inserito dallo studente, individua possibili errori
        e spiega come correggerli in modo semplice.
        """

    elif mode == 'Esercizi':
        system_prompt = """
        Sei un assistente che crea esercizi di programmazione.
        In base alla richiesta dello studente, proponi un esercizio pratico
        e spiega l'obiettivo dell'esercizio.
        """

    elif mode == 'Quiz':
        system_prompt = """
        Sei un assistente che crea quiz di programmazione.
        Genera una domanda a risposta multipla con quattro opzioni:
        A, B, C e D. Indica anche la risposta corretta e una breve spiegazione.
        """

    else:
        system_prompt = """
        Sei un assistente per lo studio della programmazione.
        Rispondi in modo semplice e chiaro.
        """

    #Invio il prompt all'API AI, se vi è errore lo gestisco 
    try:
        ai_response = client.responses.create( #Chiamo l'API

        model="gpt-4o-mini", #Scelgo il modello

        input = [

            {

                #Qui definisco il comportamento a cui si deve attenere l'API, ed è il primo messaggio che viene mandato all'API
                "role": "system", 
                "content" : system_prompt

            },

            {
                #Qui invio un secondo messaggio che rappresenta la domanda posta dall'utente
                "role": "user",
                "content" : message

            }

        ]

        )

        response_text = ai_response.output_text #Prendo la risposta finale da mostrare all'utente


        return jsonify({
            "response": response_text #Invio la risposta in formato JSON al front-end
        })

    #Nel caso di errore
    except Exception as e:
        
        return jsonify({

            "response" : f"Errore nel collegamento con l'AI: {str(e)}" #str(e) rappresenta il testo di errore restituito dall'API

        })

#Avvio del server Flask
if __name__ == '__main__':
    app.run(debug=True)