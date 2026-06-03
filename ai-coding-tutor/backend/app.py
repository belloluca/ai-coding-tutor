from flask import Flask, jsonify, request #Flask: serve per creare il server, jsonify:  per resituire oggetti JSON al front-end, request: serve per leggere i dati ricevuti dal front-end
from flask_cors import CORS #CORS: serve al frontend JavaScript di comunicare con Flask.
from google import genai #importo la libreria principale di Google GenAI
from dotenv import load_dotenv #load_dotenv: serve per leggere variabili da un file 
import os #os: serve per leggere variabili d’ambiente del sistema.

load_dotenv() #leggo il file .env che contiene la key all'API AI

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY")) #Creo il client che si collegherà con Gemini e leggo la key contenuta nella variabile "GEMINI_API_KEY" nell'ambiente .env

@app.route('/api/chat', methods=['POST']) #Permette di avviare la funzione sottostante quando il front-end riceve una richiesta con il metodo: POST
def chat():

    data = request.get_json() #Leggo i dati JSON ricevuti dal front-end

    #Distinguo il messaggio dalla modalità
    message = data.get('message', '')
    mode = data.get('mode', 'Tutor')

    #Verifico la modalità selezionata e mando un prompt inerente all'API AI
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

    #Invio il prompt all'API AI, se vi è errore lo gestisco 
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

        ai_response = client.models.generate_content(model = "gemini-2.0-flash-lite", contents = prompt) #Invio la richiesta a gemini indicando il modello ed il contenuto

        #Invio la risposta in formato JSON al front-end
        return jsonify({
            "response": ai_response.text #Conservo in response solamente il testo della risposta
        })
    
    

    #Nel caso di errore
    except Exception as e:

        return jsonify({

            "response": "Il servizio AI non è momentaneamente disponibile oppure la quota gratuita è stata superata. Riprovare più tardi."

        })

#Avvio del server Flask
if __name__ == '__main__':
    app.run(debug=True)