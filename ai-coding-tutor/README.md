# AI Coding Tutor

AI Coding Tutor è una web app pensata come progetto universitario per una tesi sull'utilizzo dell'Intelligenza Artificiale nel supporto allo studio della programmazione.

Il sistema permette allo studente di interagire con un chatbot educativo attraverso diverse modalità:

- **Tutor**: spiegazione semplice e guidata degli argomenti di programmazione.
- **Debug codice**: analisi di codice e suggerimenti per correggere errori.
- **Esercizi**: generazione di esercizi personalizzati.
- **Quiz**: creazione di domande per verificare la comprensione.

## Struttura del progetto

```text
ai-coding-tutor/
├── backend/
│   ├── app.py
│   ├── ai_service.py
│   ├── database.py
│   ├── prompts.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── database/
│   └── .gitkeep
│
├── sperimentazione/
│   ├── questionario_utenti.docx
│   ├── risultati_test.xlsx
│   └── grafici/
│
├── docs/
│   ├── descrizione_progetto.md
│   └── screenshot/
│
├── README.md
└── .gitignore
```

## Tecnologie utilizzate

- HTML
- CSS
- JavaScript
- Python
- Flask
- SQLite

## Avvio del progetto

### 1. Avviare il back-end

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Il server Flask sarà disponibile su:

```text
http://localhost:5000
```

### 2. Avviare il front-end

Aprire il file:

```text
frontend/index.html
```

nel browser.

## Possibili sviluppi futuri

- Collegamento a una vera API AI.
- Inserimento di documenti didattici per creare una modalità RAG.
- Salvataggio avanzato dello storico delle conversazioni.
- Dashboard per visualizzare dati e risultati della sperimentazione.
- Questionario utenti per valutare utilità, chiarezza e qualità delle risposte.

## Obiettivo del progetto

L'obiettivo è realizzare un prototipo funzionante di chatbot educativo capace di supportare lo studente nello studio del coding, mostrando come l'AI possa essere utilizzata in ambito formativo.
