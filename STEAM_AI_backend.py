from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import requests
import fitz

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key="sk-apikey")

response = requests.get("https://drive.google.com/uc?export=download&id=1gcKh-CSbVJYg1Q9A-gAyl-owhUfTkn5C")
pdf_content = response.content

with open('temp.pdf', 'wb') as f:
    f.write(pdf_content)

documento = fitz.open('temp.pdf')

prompt = ""
for pagina in documento:
    prompt += pagina.get_text()

documento.close()

@app.route('/send_message_to_bot', methods=['POST'])
def chat():
    print(f"Ricevuta richiesta da \"{request.remote_addr}\"")
    data = request.get_json()

    if not data or 'messages' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    messages = data['messages']
    print(f"{request.remote_addr}: {messages[-1]['content']}")
    messages.insert(0, {"role": "system", "content": prompt[:len(prompt)]})
    try:
        full_response = ""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            stream=True
        )
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content

        print(f"STEAM AI: {full_response}")
        return jsonify({'response': full_response}), 200
    except Exception as e:
        print(f"error:\n{e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8155, debug=True)