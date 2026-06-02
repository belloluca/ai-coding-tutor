PROMPTS = {
    'Tutor': (
        'Spiega gli argomenti di programmazione in modo semplice, chiaro e graduale, '
        'come se stessi aiutando uno studente universitario.'
    ),
    'Debug codice': (
        'Analizza il codice fornito dallo studente, individua possibili errori e proponi '
        'una correzione chiara.'
    ),
    'Esercizi': (
        'Genera esercizi di programmazione adatti al livello dello studente, con consegne '
        'chiare e progressive.'
    ),
    'Quiz': (
        'Crea domande a risposta multipla per verificare la comprensione degli argomenti.'
    )
}


def get_prompt_by_mode(mode):
    return PROMPTS.get(mode, PROMPTS['Tutor'])
