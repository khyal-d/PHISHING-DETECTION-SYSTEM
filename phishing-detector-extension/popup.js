// popup.js
import { checkUrlWithApi } from "./api.js";

const urlInput   = document.getElementById("urlInput");
const checkBtn   = document.getElementById("checkButton");
const statusEl   = document.getElementById("status");
const resultEl   = document.getElementById("result");

// Pre-fill with current tab's URL
document.addEventListener("DOMContentLoaded", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const activeTab = tabs[0];
    if (activeTab && activeTab.url) {
      urlInput.value = activeTab.url;
    }
  });
});

checkBtn.addEventListener("click", async () => {
  const url = urlInput.value.trim();
  if (!url) {
    statusEl.textContent = "Please enter a URL.";
    resultEl.innerHTML = "";
    return;
  }

  statusEl.textContent = "Checking...";
  resultEl.innerHTML = "";

  try {
    const data = await checkUrlWithApi(url);
    // data: { label: "legitimate", phishing_probability: 0.34 }

    statusEl.textContent = "";
    const probPercent = (data.phishing_probability * 100).toFixed(2);

    const labelClass = data.label === "phishing" ? "label-bad" : "label-good";

    resultEl.innerHTML = `
      <div class="label ${labelClass}">${data.label}</div>
      <div class="prob">Phishing probability: ${probPercent}%</div>
    `;
  } catch (err) {
    console.error(err);
    statusEl.textContent = "Error contacting API.";
    resultEl.innerHTML = `<div class="error">${err.message}</div>`;
  }
});
