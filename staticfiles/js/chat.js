document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".chat-container");
  if (!container) return;

  // 🔹 Element references
  const conversationId = container.dataset.conversationId;
  const userId = parseInt(container.dataset.userId || window.userId);
  const messagesContainer = document.getElementById("messages");
  const messageInput = document.getElementById("messageInput");
  const sendBtn = document.getElementById("sendBtn");
  const uploadForm = document.getElementById("uploadForm");

  // 🔹 WebSocket setup
  const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
  const ws = new WebSocket(`${wsScheme}://${window.location.host}/ws/chat/${conversationId}/`);

  // 🔹 Scroll helper
  const scrollToBottom = () => {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  };

  // 🔹 Escape HTML safely
  const escapeHtml = (text) => {
    const div = document.createElement("div");
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
  };

  // 🔹 Render message bubble
  const renderMessage = (m, isSelf = false) => {
    const el = document.createElement("div");
    el.className = "chat-message " + (isSelf ? "self" : "other");

    const avatar = `<div class="avatar">${m.sender_username?.[0]?.toUpperCase() || "?"}</div>`;
    const body = `
      <div class="bubble">
        <div class="meta">
          <strong>${m.sender_username || "User"}</strong>
          <small>${new Date(m.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</small>
        </div>
        <div class="text">${escapeHtml(m.content || "")}</div>
      </div>
    `;

    el.innerHTML = avatar + body;
    messagesContainer.appendChild(el);
    scrollToBottom();
  };

  // 🔹 Send text message
  const sendText = () => {
    const text = messageInput.value.trim();
    if (!text) return;

    // Optimistic local display
    renderMessage({
      sender_username: "You",
      content: text,
      created_at: new Date().toISOString(),
    }, true);

    ws.send(JSON.stringify({ type: "message.send", text }));
    messageInput.value = "";
  };

  // 🔹 WebSocket events
  ws.onopen = () => console.log("✅ WebSocket connected");
  ws.onerror = (err) => console.error("❌ WebSocket error:", err);
  ws.onclose = () => console.warn("⚠️ WebSocket disconnected");

  ws.onmessage = (e) => {
    try {
      const data = JSON.parse(e.data);

      if (data.type === "message.broadcast") {
        const m = data.message;
        renderMessage({
          sender_username: m.sender_username,
          content: m.content,
          created_at: m.created_at,
        }, m.sender_id === userId);
      } else if (data.type === "typing") {
        showTyping(data.username);
      }
    } catch (err) {
      console.error("WS parse error:", err);
    }
  };

  // 🔹 Typing indicator
  let typingTimeout;
  const showTyping = (username) => {
    clearTimeout(typingTimeout);
    let indicator = document.getElementById("typingIndicator");

    if (!indicator) {
      indicator = document.createElement("div");
      indicator.id = "typingIndicator";
      indicator.className = "typing-indicator";
      messagesContainer.appendChild(indicator);
    }

    indicator.textContent = `${username} is typing...`;
    scrollToBottom();

    typingTimeout = setTimeout(() => {
      indicator.remove();
    }, 1500);
  };

  // 🔹 Input events
  sendBtn.addEventListener("click", sendText);
  messageInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendText();
    } else {
      ws.send(JSON.stringify({ type: "typing" }));
    }
  });

// 🔹 File upload handler (fixed)
uploadForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(uploadForm);

  try {
    const response = await fetch(uploadForm.action, {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json",
      },
    });

    // Try to parse JSON safely
    const text = await response.text();
    let data;

    try {
      data = JSON.parse(text);
    } catch {
      console.error("⚠️ Response not JSON:", text);
      return;
    }

    // ✅ Successfully uploaded
    if (data.success && data.html) {
      messagesContainer.insertAdjacentHTML("beforeend", data.html);
      scrollToBottom();
      uploadForm.reset();
      messageInput.value = "";
    } 
    // ⚠️ Handle error messages
    else if (data.error) {
      alert(data.error);
    } 
    // ⚠️ Unexpected data
    else {
      console.warn("Unexpected response:", data);
    }

  } catch (err) {
    console.error("Upload failed:", err);
  }
});
});