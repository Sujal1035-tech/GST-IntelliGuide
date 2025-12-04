// Use current domain for API calls (works both locally and in production)
const API_BASE = window.location.origin;

let currentChatId = null;
let currentSocket = null;

// DOM elements
const chatsListEl = document.getElementById("chats-list");
const chatBoxEl = document.getElementById("chat-box");
const chatTitleEl = document.getElementById("chat-title");
const msgInputEl = document.getElementById("message-input");
const sendBtnEl = document.getElementById("send-btn");
const newChatBtnEl = document.getElementById("new-chat-btn");
const typingEl = document.getElementById("typing-indicator");
const logoutBtnEl = document.getElementById("logout-btn");
const darkToggleEl = document.getElementById("dark-mode-toggle");

// ---------- Helpers ----------
function formatTime(ts) {
  const d = ts ? new Date(ts) : new Date();
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function setTyping(state) {
  typingEl.style.display = state ? "flex" : "none";
}

function clearMessages() {
  chatBoxEl.innerHTML = "";
}

function addMessage(text, sender = "user", timestamp = null) {
  const row = document.createElement("div");
  row.classList.add("message-row");
  row.classList.add(sender === "user" ? "user-message" : "bot-message");

  const meta = document.createElement("div");
  meta.classList.add("message-meta");
  meta.textContent =
    (sender === "user" ? "You" : "GST AI") + " • " + formatTime(timestamp);

  const bubble = document.createElement("div");
  bubble.classList.add("bubble");

  // For bot messages, render markdown-like formatting
  if (sender === "bot") {
    bubble.innerHTML = formatBotMessage(text);
  } else {
    bubble.textContent = text;
  }

  row.appendChild(meta);
  row.appendChild(bubble);
  chatBoxEl.appendChild(row);
  chatBoxEl.scrollTop = chatBoxEl.scrollHeight;
}

// Format bot message with basic markdown rendering
function formatBotMessage(text) {
  // Escape HTML to prevent XSS
  let formatted = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Convert **text** to bold
  formatted = formatted.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");

  // Convert newlines to <br>
  formatted = formatted.replace(/\n/g, "<br>");

  // Style bullet points
  formatted = formatted.replace(/• /g, '<span class="bullet">•</span> ');

  return formatted;
}

// ---------- Dark mode ----------
function initDarkMode() {
  const saved = localStorage.getItem("gst_dark_mode");
  if (saved === "true") {
    document.body.classList.add("dark");
    darkToggleEl.checked = true;
  }

  darkToggleEl.addEventListener("change", () => {
    if (darkToggleEl.checked) {
      document.body.classList.add("dark");
      localStorage.setItem("gst_dark_mode", "true");
    } else {
      document.body.classList.remove("dark");
      localStorage.setItem("gst_dark_mode", "false");
    }
  });
}

// ---------- API calls ----------
async function fetchJSON(path) {
  const res = await fetch(API_BASE + path, {
    credentials: "include",
  });
  if (!res.ok) return null;
  return await res.json();
}

async function checkAuth() {
  const me = await fetchJSON("/auth/me");
  if (!me) {
    window.location.href = "/frontend/login.html";
    return;
  }
  const email = me.email || "user@example.com";
  document.getElementById("user-email").textContent = email;
  document.getElementById("user-name").textContent = "GST User";
  document.getElementById("user-avatar").textContent = (email[0] || "U").toUpperCase();
}

async function loadChats() {
  const chats = await fetchJSON("/chats/");
  if (!Array.isArray(chats)) return;

  chatsListEl.innerHTML = "";
  chats.forEach((chat) => {
    const el = document.createElement("div");
    el.classList.add("chat-item");
    el.dataset.id = chat._id;
    el.textContent = chat.title || "Untitled chat";
    el.addEventListener("click", () => {
      selectChat(chat._id, chat.title || "Untitled chat");
    });
    chatsListEl.appendChild(el);
  });
}

function highlightChat(chatId) {
  const items = document.querySelectorAll(".chat-item");
  items.forEach((el) => {
    if (el.dataset.id === chatId) el.classList.add("active");
    else el.classList.remove("active");
  });
}

async function loadMessages(chatId) {
  const msgs = await fetchJSON(`/chats/${chatId}/messages`);
  clearMessages();
  if (!Array.isArray(msgs)) return;

  msgs.forEach((m) => {
    const sender = m.sender === "user" ? "user" : "bot";
    addMessage(m.content, sender, m.timestamp);
  });
}

// ---------- WebSocket ----------
function connectWebSocket(chatId) {
  if (currentSocket) {
    currentSocket.close();
  }

  // Use wss:// for HTTPS, ws:// for HTTP
  const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${wsProtocol}//${window.location.host}/ws/chat/${chatId}`;
  const ws = new WebSocket(wsUrl);
  currentSocket = ws;

  ws.onopen = () => {
    console.log("WebSocket connected:", wsUrl);
  };

  ws.onmessage = (event) => {
    // assuming backend sends plain text response
    setTyping(false);
    addMessage(event.data, "bot", new Date().toISOString());
  };

  ws.onclose = () => {
    console.log("WebSocket closed");
  };

  ws.onerror = (err) => {
    console.error("WebSocket error:", err);
  };
}

// ---------- Chat controls ----------
async function selectChat(chatId, title) {
  currentChatId = chatId;
  chatTitleEl.textContent = title;
  highlightChat(chatId);
  await loadMessages(chatId);
  connectWebSocket(chatId);
}

async function createChat() {
  const title = prompt("Chat title:", "New GST Chat") || "New GST Chat";
  const params = new URLSearchParams({ title });

  const res = await fetch(`${API_BASE}/chats/?${params}`, {
    method: "POST",
    credentials: "include",
  });

  if (!res.ok) {
    alert("Failed to create chat");
    return;
  }

  const chat = await res.json();
  await loadChats();
  await selectChat(chat._id, chat.title || "Untitled chat");
}

function sendMessage() {
  const text = msgInputEl.value.trim();
  if (!text || !currentSocket || currentSocket.readyState !== WebSocket.OPEN) {
    return;
  }

  addMessage(text, "user", new Date().toISOString());
  msgInputEl.value = "";
  setTyping(true);

  // send plain text (backend expects raw text)
  currentSocket.send(text);
}

// ---------- Logout ----------
async function logout() {
  await fetch(`${API_BASE}/logout`, {
    method: "POST",
    credentials: "include",
  });
  window.location.href = "/frontend/login.html";
}

// ---------- Init ----------
function initEvents() {
  sendBtnEl.addEventListener("click", sendMessage);
  msgInputEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });
  newChatBtnEl.addEventListener("click", createChat);
  logoutBtnEl.addEventListener("click", logout);
}

async function init() {
  initDarkMode();
  initEvents();
  await checkAuth();
  await loadChats();
}

init();
