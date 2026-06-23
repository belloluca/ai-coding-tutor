const utenteLoggato = JSON.parse(localStorage.getItem("utenteLoggato"));

if (!utenteLoggato) {
    alert("Devi effettuare il login per accedere alla chat.");
    window.location.href = "login.html";
}

const chatForm = document.getElementById('chatForm'); 
const messageInput = document.getElementById('messageInput'); 
const chatMessages = document.getElementById('chatMessages'); 
const modeButtons = document.querySelectorAll('.mode-btn'); 
const historyList = document.getElementById("historyList"); 
const newChatBtn = document.getElementById("newChatBtn"); 
const logoutBtn = document.getElementById("logoutBtn"); 

let selectedMode = 'Tutor'; 

modeButtons.forEach(button => {
    button.addEventListener('click', () => { 
        modeButtons.forEach(btn => btn.classList.remove('active')); 
        button.classList.add('active'); 
        selectedMode = button.dataset.mode; 
    });
});

chatForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const utente = JSON.parse(localStorage.getItem("utenteLoggato"));

    if (!utente) {
        alert("Devi effettuare il login.");
        window.location.href = "login.html";
        return;
    }

    const message = messageInput.value.trim(); 
    if (!message) return; 

    addMessage('Studente', message, 'user-message'); 
    messageInput.value = ''; 

    const thinkingMessage = addMessage('AI Tutor', 'Sta pensando...', 'ai-message');

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

        const data = await response.json(); 
        
        thinkingMessage.remove();

        addMessage('AI Tutor', data.response || 'Errore nella risposta.', 'ai-message', selectedMode);
        caricaStorico();
    } catch (error) {
        thinkingMessage.remove();
        addMessage('Sistema', 'Impossibile collegarsi al server Flask.', 'ai-message');
    }
});


function addMessage(sender, text, className, mode = null) {
    const messageDiv = document.createElement('div'); 
    messageDiv.classList.add('message', className); 

    messageDiv.innerHTML = `
        <strong>${sender}</strong>
        ${mode ? `<span class="mode-label">${mode}</span>` : ""}
        <p>${text}</p>
    `;

    chatMessages.appendChild(messageDiv);

    chatMessages.scrollTop = chatMessages.scrollHeight;

    return messageDiv;
}


async function caricaStorico() {

    const utente = JSON.parse(localStorage.getItem("utenteLoggato"));

    if (!utente) return;

    const response = await fetch(`http://127.0.0.1:5000/api/history/${utente.id}`);

    const history = await response.json();

    historyList.innerHTML = "";

    history.forEach(chat => {

        const item = document.createElement("div");
        item.classList.add("history-item");

        item.innerHTML = `
            <div class="history-content">
                <strong>${chat.modalita}</strong>
                <span>${chat.creato_il}</span>
            </div>

            <button class="delete-chat-btn">🗑</button>
        `;

        item.addEventListener("click", () => {
            chatMessages.innerHTML = "";

            addMessage("Studente", chat.messaggio_utente, "user-message");
            addMessage("AI Tutor", chat.risposta_ai, "ai-message", chat.modalita);
        });

        const deleteBtn = item.querySelector(".delete-chat-btn");

        deleteBtn.addEventListener("click", async (event) => {
            event.stopPropagation();

            await fetch(`http://127.0.0.1:5000/api/delete-chat/${chat.id}`, {
                method: "DELETE"
            });

            caricaStorico();
        });

        historyList.appendChild(item);
    });

}

newChatBtn.addEventListener("click", () => {
    chatMessages.innerHTML = "";

    addMessage("AI Tutor", "Come posso aiutarti?", "ai-message");

    messageInput.value = "";
});

logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("utenteLoggato");
    window.location.href = "login.html";
});

caricaStorico();