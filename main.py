from flask import Flask, request, jsonify 
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "🧠 ChatGPT API is running!"

@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Missing prompt'}), 400

    try:
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openrouter/auto",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        if response.status_code != 200:
            return jsonify({"error": f"{response.status_code} - {response.text}"}), 500

        completion = response.json()['choices'][0]['message']['content']
        return jsonify({'response': completion})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
