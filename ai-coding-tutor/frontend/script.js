const chatForm = document.getElementById('chatForm'); // Il form della chat
const messageInput = document.getElementById('messageInput'); // Il campo dove viene scritto il messaggio
const chatMessages = document.getElementById('chatMessages'); // Il contenitore dove vengono mostrati i messaggi
const modeButtons = document.querySelectorAll('.mode-btn'); // I pulsanti con le varie modalità

let selectedMode = 'Tutor'; // Selezione come modalità predefinita 'Tutor'

// Gestisco il cambio di modalità
modeButtons.forEach(button => {
    button.addEventListener('click', () => { // Identifico quale pulsante viene cliccato
        modeButtons.forEach(btn => btn.classList.remove('active')); // Rimuovo la classe 'active' da tutti i pulsanti
        button.classList.add('active'); // Aggiungo 'active' solo al pulsate cliccato
        selectedMode = button.dataset.mode; // Aggiorno la modalità selezionata
    });
});

// Quando il form viene inviato viene eseguita la funzione sottostante
chatForm.addEventListener('submit', async (event) => {
    event.preventDefault(); // Impedisce al browser di ricaricare la pagina all'invio del form

    // Raccolgo le informazioni riguardanti l'utente
    const utente = JSON.parse(localStorage.getItem("utenteLoggato"));

    // Verifico che l'utente sia loggato
    if (!utente) {
        alert("Devi effettuare il login.");
        window.location.href = "login.html";
        return;
    }

    const message = messageInput.value.trim(); // Rimuovo tutti gli spazi iniziali e finali
    if (!message) return; // Se il messaggio è vuoto esco dalla funzione

    addMessage('Studente', message, 'user-message'); // Mostro nella chat il messaggio dello studente
    messageInput.value = ''; // Svuoto l'input

    // Messaggio temporaneo
    const thinkingMessage = addMessage('AI Tutor', 'Sta pensando...', 'ai-message');

    // Effettuo una richiesta HTTP POST al server Flask nel formato JSON
    try {
        const response = await fetch('http://localhost:5000/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                mode: selectedMode,
                user_id: utente.id
            })
        });

        const data = await response.json(); // Leggo la risposta ricevuta dal server Flask
        
        // Rimuovo il messaggio temporaneo
        thinkingMessage.remove();

        // Mostro la risposta nella chat, e nel caso di errore la gestisco
        addMessage('AI Tutor', data.response || 'Errore nella risposta.', 'ai-message', selectedMode);
    } catch (error) {
        thinkingMessage.remove();
        addMessage('Sistema', 'Impossibile collegarsi al server Flask.', 'ai-message');
    }
});

// Con questa funzione creo il messaggio HTML da mostrare in chat
function addMessage(sender, text, className, mode = null) {
    const messageDiv = document.createElement('div'); // Crea un nuovo elemento HTML <div>, cioè il contenitore del messaggio.
    messageDiv.classList.add('message', className); // Aggiunge al div due classi CSS:

    // Inserisce dentro al div il contenuto del messaggio.
    messageDiv.innerHTML = `
        <strong>${sender}</strong>
        ${mode ? `<span class="mode-label">${mode}</span>` : ""}
        <p>${text}</p>
    `;

    // Aggiunge il messaggio dentro il contenitore della chat
    chatMessages.appendChild(messageDiv);
    // Fa scorrere automaticamente la chat verso il basso, così l’ultimo messaggio è sempre visibile
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Restituisce il messaggio creato
    return messageDiv;
}

// Funzione che carica lo storico delle chat dell'utente
async function caricaStorico() {

    // Salvo le informazioni che ha effettuato il login
    const utente = JSON.parse(localStorage.getItem("utenteLoggato"));

    // Verifico che l'utente esista
    if (!utente) return;

    // Attendo e salvo la risposta con lo storico da parte del server Flask
    const response = await fetch(`http://127.0.0.1:5000/api/history/${utente.id}`);
    // Converto la risposta ricevuta dal server Flask in formato JSON
    const history = await response.json();

    // Mostro in console le varie chat
    console.log(history);
}

caricaStorico();