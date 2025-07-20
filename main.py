
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Get the API key securely from environment variables
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route('/')
def home():
    return "✅ ChatGPT-like API is live!"

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    if not OPENROUTER_API_KEY:
        return jsonify({"error": "API key not found in environment"}), 500

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourapp.fly.dev",   # 🔁 Replace with your actual Fly.io URL
        "X-Title": "MyChatPlatform"
    }

    payload = {
        "model": "openchat/openchat-3.5-0106",  # ✅ Valid OpenRouter model
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )

        data = response.json()

        if response.status_code != 200:
            return jsonify({"error": data.get("error", "Unknown error")}), response.status_code

        return jsonify({
            "reply": data["choices"][0]["message"]["content"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
