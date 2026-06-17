// Seleziona il form di registrazione tramite il suo id.
const form = document.querySelector("#FormRegistrazione");

// Seleziona l'elemento HTML utilizzato per mostrare messaggi
// di errore o di successo all'utente.
const feedback = document.querySelector("#feedback");

// Viene eseguito quando l'utente preme il pulsante "Registrati".
form.addEventListener("submit", async function(event) {

  // Impedisce il comportamento predefinito del form,
  // evitando il ricaricamento della pagina.
  event.preventDefault();

  // Messaggio di debug visualizzato nella console del browser.
  console.log("Form inviato");

  // Recupera i dati inseriti nel form.
  // trim() elimina eventuali spazi iniziali e finali.
  const nome = form.nome.value.trim();
  const email = form.email.value.trim();
  const password = form.password.value;

  // Controlla se la checkbox della privacy è stata selezionata.
  const privacy = form.privacy.checked;

  // Ripristina la classe CSS del messaggio di feedback.
  feedback.className = "feedback";

  // Verifica che tutti i campi obbligatori siano compilati.
  if (!nome || !email || !password) {
    feedback.textContent = "Compila tutti i campi.";
    feedback.classList.add("error");
    return;
  }

  // Controlla che l'utente abbia accettato il trattamento dei dati.
  if (!privacy) {
    feedback.textContent = "Devi accettare il trattamento dei dati.";
    feedback.classList.add("error");
    return;
  }

  // Invia i dati al back-end Flask tramite una richiesta HTTP POST.
  const response = await fetch("http://127.0.0.1:5000/api/register", {

    // Specifica il metodo HTTP utilizzato.
    method: "POST",

    // Indica che i dati inviati sono in formato JSON.
    headers: {
        "Content-Type": "application/json"
    },

    // Converte l'oggetto JavaScript in formato JSON
    // e lo inserisce nel corpo della richiesta.
    body: JSON.stringify({
        nome: nome,
        email: email,
        password: password
    })
  });

  // Attende e converte la risposta del server in un oggetto JavaScript.
  const data = await response.json();

  // Se il server restituisce un errore (es. email già registrata),
  // mostra il messaggio ricevuto e interrompe l'esecuzione.
  if (!response.ok) {
    feedback.textContent = data.error;
    feedback.classList.add("error");
    return;
  }

  // Se la registrazione è avvenuta con successo,
  // mostra il messaggio restituito dal server.
  feedback.textContent = data.message;
  feedback.classList.add("success");

  // Svuota tutti i campi del form.
  form.reset();

  // Questa parte è ridondante perché il messaggio e il reset
  // sono già stati eseguiti nelle righe precedenti.
  // Può essere eliminata senza modificare il funzionamento.
  feedback.textContent = "Registrazione completata. Ora puoi effettuare il login.";
  feedback.classList.add("success");

  form.reset();

});