// api.js
const API_BASE_URL = "http://127.0.0.1:8000";

export async function checkUrlWithApi(url) {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ url })
  });

  if (!response.ok) {
    const text = await response.text().catch(() => "");
    throw new Error(`API error (${response.status}): ${text || response.statusText}`);
  }

  return response.json(); // { label: "...", phishing_probability: 0.34 }
}
