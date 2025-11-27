const API_BASE = "http://localhost:8001";

document.getElementById("register-btn").addEventListener("click", registerUser);

async function registerUser() {
  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();
  const errorEl = document.getElementById("register-error");

  errorEl.textContent = "";

  if (!name || !email || !password) {
    errorEl.textContent = "All fields are required.";
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password }),
    });

    if (res.ok) {
      alert("Registration successful! Please login.");
      window.location.href = "/frontend/login.html";
    } else {
      const data = await res.json();
      errorEl.textContent = data.detail || "Registration failed.";
    }

  } catch (err) {
    console.error(err);
    errorEl.textContent = "Network error";
  }
}
