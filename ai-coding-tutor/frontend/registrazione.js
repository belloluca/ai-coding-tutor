const form = document.querySelector("#FormRegistrazione");
const feedback = document.querySelector("#feedback");

form.addEventListener("submit", async function(event) {

  event.preventDefault();

  console.log("Form inviato");

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

  const response = await fetch("http://127.0.0.1:5000/api/register", {

    method: "POST",

    headers: {
        "Content-Type": "application/json"
    },

    body: JSON.stringify({
        nome: nome,
        email: email,
        password: password
    })
  });

  const data = await response.json();

  if (!response.ok) {
    feedback.textContent = data.error;
    feedback.classList.add("error");
    return;
  }

  feedback.textContent = data.message;
  feedback.classList.add("success");

  form.reset();

});