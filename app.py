from flask import Flask, request, jsonify
import requests
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {app.config["OPENAI_API_KEY"]}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'gpt-4',  # Replace with the appropriate model
                'messages': [{'role': 'user', 'content': prompt}]
            }
        )

        response.raise_for_status()
        result = response.json()
        message = result['choices'][0]['message']['content']

        return jsonify({'message': message})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
