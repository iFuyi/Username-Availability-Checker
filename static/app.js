const usernameInput = document.getElementById("username");
const checkButton = document.getElementById("check-btn");
const resultsCard = document.getElementById("results-card");
const resultsBody = document.getElementById("results-body");
const loadingEl = document.getElementById("loading");
const errorEl = document.getElementById("error");
const copyBtn = document.getElementById("copy-btn");
const downloadBtn = document.getElementById("download-btn");

let lastPayload = null;

const usernamePattern = /^[A-Za-z0-9_.]{2,30}$/;

function setLoading(isLoading) {
  loadingEl.hidden = !isLoading;
  checkButton.disabled = isLoading;
}

function showError(message) {
  errorEl.textContent = message;
  errorEl.hidden = !message;
}

function statusClass(status) {
  if (status === "available") return "status-available";
  if (status === "taken") return "status-taken";
  return "status-unknown";
}

function renderResults(payload) {
  resultsBody.innerHTML = "";
  payload.results.forEach((item) => {
    const row = document.createElement("tr");

    const platformCell = document.createElement("td");
    platformCell.textContent = item.platform;

    const statusCell = document.createElement("td");
    statusCell.textContent = item.status;
    statusCell.className = statusClass(item.status);

    const linkCell = document.createElement("td");
    if (item.url) {
      const link = document.createElement("a");
      link.href = item.url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = item.status === "taken" ? item.url : "View";
      linkCell.appendChild(link);
    } else {
      linkCell.textContent = "-";
    }

    const notesCell = document.createElement("td");
    notesCell.textContent = item.reason || "";

    row.appendChild(platformCell);
    row.appendChild(statusCell);
    row.appendChild(linkCell);
    row.appendChild(notesCell);
    resultsBody.appendChild(row);
  });

  resultsCard.hidden = false;
  copyBtn.disabled = false;
  downloadBtn.disabled = false;
}

async function checkUsername() {
  const username = usernameInput.value.trim();

  if (!usernamePattern.test(username)) {
    showError("Use 2-30 characters: letters, numbers, underscore, or dot.");
    return;
  }

  showError("");
  setLoading(true);

  try {
    const response = await fetch(`/api/check?username=${encodeURIComponent(username)}`);
    const data = await response.json();

    if (!response.ok) {
      const message = data?.detail || "Something went wrong.";
      showError(message);
      resultsCard.hidden = true;
      return;
    }

    lastPayload = data;
    renderResults(data);
  } catch (err) {
    showError("Network error. Please try again.");
  } finally {
    setLoading(false);
  }
}

async function copyJson() {
  if (!lastPayload) return;
  const text = JSON.stringify(lastPayload, null, 2);

  try {
    await navigator.clipboard.writeText(text);
    showError("Copied JSON to clipboard.");
    setTimeout(() => showError(""), 2000);
  } catch (err) {
    showError("Clipboard unavailable. Try downloading instead.");
  }
}

function downloadJson() {
  if (!lastPayload) return;
  const text = JSON.stringify(lastPayload, null, 2);
  const blob = new Blob([text], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `handle-scout-${lastPayload.username}.json`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

checkButton.addEventListener("click", checkUsername);
usernameInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    checkUsername();
  }
});
copyBtn.addEventListener("click", copyJson);
downloadBtn.addEventListener("click", downloadJson);
