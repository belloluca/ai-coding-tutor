const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const chatMessages = document.getElementById('chatMessages');
const modeButtons = document.querySelectorAll('.mode-btn');

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

    const message = messageInput.value.trim();
    if (!message) return;

    addMessage('Studente', message, 'user-message');
    messageInput.value = '';

    try {
        const response = await fetch('http://localhost:5000/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                mode: selectedMode
            })
        });

        const data = await response.json();
        addMessage('AI Tutor', data.response || 'Errore nella risposta.', 'ai-message');
    } catch (error) {
        addMessage('Sistema', 'Impossibile collegarsi al server Flask.', 'ai-message');
    }
});

function addMessage(author, text, className) {
    const messageBox = document.createElement('div');
    messageBox.className = `message ${className}`;

    const title = document.createElement('strong');
    title.textContent = author;

    const paragraph = document.createElement('p');
    paragraph.textContent = text;

    messageBox.appendChild(title);
    messageBox.appendChild(paragraph);
    chatMessages.appendChild(messageBox);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
