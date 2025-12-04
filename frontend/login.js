// Use current domain for API calls (works both locally and in production)
const API_BASE = window.location.origin;

document.getElementById("login-btn").addEventListener("click", loginUser);

async function loginUser() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();
  const errorEl = document.getElementById("login-error");
  errorEl.textContent = "";

  if (!email || !password) {
    errorEl.textContent = "Please enter email and password.";
    return;
  }

  const url = `${API_BASE}/login?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`;

  try {
    const res = await fetch(url, {
      method: "POST",
      credentials: "include",
    });

    if (!res.ok) {
      errorEl.textContent = "Invalid credentials.";
      return;
    }

    window.location.href = "/frontend/chat.html";
  } catch (err) {
    console.error(err);
    errorEl.textContent = "Network error. Check if backend is running.";
  }
}
