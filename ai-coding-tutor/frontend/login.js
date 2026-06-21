const form = document.querySelector("#FormLogin"); 
const feedback = document.querySelector("#feedback"); 


form.addEventListener("submit", async function(event) {
  event.preventDefault(); 

  const email = form.email.value.trim(); 
  const password = form.password.value; 

  feedback.className = "feedback"; 

  if (!email || !password) {
    feedback.textContent = "Compila tutti i campi.";
    feedback.classList.add("error");
    return;
  }

  const response = await fetch("http://127.0.0.1:5000/api/login", {

    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
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

  localStorage.setItem("utenteLoggato", JSON.stringify(data.user));

  setTimeout(() => {
    window.location.href = "index.html";
  }, 1000);
});