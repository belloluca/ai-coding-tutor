const form = document.querySelector("#FormLogin"); // Raccoglie i dati del form: email e password
const feedback = document.querySelector("#feedback"); // Raccoglie il risultato del feedback

// Viene eseguita quando si invia il form
form.addEventListener("submit", async function(event) {
  event.preventDefault(); // Evita che la pagina si ricarichi all'invio del form

  const email = form.email.value.trim(); // Si salva l'email senza spazi iniziali e finali
  const password = form.password.value; // Si salva la password

  feedback.className = "feedback"; 

  // Si controlla che i campi email e password sono riempiti  
  if (!email || !password) {
    feedback.textContent = "Compila tutti i campi.";
    feedback.classList.add("error");
    return;
  }

  // Si inviano i dati prelevati al server Flask, si attende la risposta, e si restituisci la risposta
  const response = await fetch("http://127.0.0.1:5000/api/login", {

    // Viene specificata la tipologia di richiesta
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      email: email,
      password: password
    })
  });

  // Converte la risposta del server in formato JSON
  const data = await response.json();


  // Se le credenziali sono errate restituirà un messaggio d'errore
  if (!response.ok) {
    feedback.textContent = data.error;
    feedback.classList.add("error");
    return;
  }

  // Nel caso di credenziali valide
  feedback.textContent = data.message;
  feedback.classList.add("success");

  // Salva nel localStorage i dati dell'utente loggato
  localStorage.setItem("utenteLoggato", JSON.stringify(data.user));

  // L'utente viene indirizzato alla pagina "index.html"
  setTimeout(() => {
    window.location.href = "index.html";
  }, 1000);
});