from prompts import get_prompt_by_mode


def generate_ai_response(user_message, mode):
    """
    Funzione che genera la risposta del chatbot.

    In questa versione iniziale la risposta è simulata, così puoi sviluppare
    e testare il front-end senza dover collegare subito un'API esterna.

    Successivamente potrai sostituire questa parte con una chiamata reale
    a un modello AI tramite API.
    """
    system_prompt = get_prompt_by_mode(mode)

    if mode == 'Debug codice':
        return (
            "Analisi del codice ricevuto:\n"
            "1. Controlla la sintassi.\n"
            "2. Verifica le variabili dichiarate.\n"
            "3. Controlla eventuali errori logici.\n\n"
            "Esempio di suggerimento: prova a stampare i valori intermedi "
            "per capire dove si genera l'errore."
        )

    if mode == 'Esercizi':
        return (
            "Esercizio proposto:\n"
            "Scrivi una funzione in C++ che riceve un numero intero e restituisce "
            "true se il numero è pari, false altrimenti."
        )

    if mode == 'Quiz':
        return (
            "Quiz:\n"
            "Quale tra questi elementi permette di ripetere un blocco di codice?\n"
            "A) if\nB) for\nC) return\nD) include\n\n"
            "Risposta corretta: B) for"
        )

    return (
        f"Modalità attiva: {mode}\n\n"
        f"Prompt utilizzato: {system_prompt}\n\n"
        "Spiegazione: una funzione in C++ è un blocco di codice riutilizzabile "
        "che svolge un compito specifico. Permette di rendere il programma più "
        "ordinato, leggibile e modulare."
    )
