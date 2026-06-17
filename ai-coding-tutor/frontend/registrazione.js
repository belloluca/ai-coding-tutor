const form = document.querySelector("#FormRegistrazione");
const feedback = document.querySelector("#feedback");

form.addEventListener("submit", function(event) {
  event.preventDefault();

  const nome = form.nome.value.trim();
  const email = form.email.value.trim();
  const password = form.password.value;
  const privacy = form.privacy.checked;

  feedback.className = "feedback";

  if (!nome || !email || !password) {
    feedback.textContent = "Compila tutti i campi.";
    feedback.classList.add("error");
    return;
  }

  if (!privacy) {
    feedback.textContent = "Devi accettare il trattamento dei dati.";
    feedback.classList.add("error");
    return;
  }

  localStorage.setItem("utenteChatbot", JSON.stringify({
    nome: nome,
    email: email,
    password: password
  }));

  feedback.textContent = "Registrazione completata. Ora puoi effettuare il login.";
  feedback.classList.add("success");

  form.reset();
});