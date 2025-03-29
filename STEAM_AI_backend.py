from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import requests
import docx
from io import BytesIO

app = Flask(__name__)
CORS(app)

client = Groq(api_key="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")

# Scarica il file DOCX con header appropriato
headers = {"User-Agent": "Mozilla/5.0"}
url = "https://drive.google.com/uc?export=download&id=1gcKh-CSbVJYg1Q9A-gAyl-owhUfTkn5C"
response = requests.get(url, headers=headers)

file_content = response.content

# Verifica che il contenuto sia un file DOCX (gli archivi ZIP iniziano con "PK")
if not file_content.startswith(b"PK"):
    raise ValueError("Contenuto scaricato non valido: non sembra essere un file DOCX.")

# Apri il documento DOCX direttamente dalla memoria usando BytesIO
document = docx.Document(BytesIO(file_content))

prompt = ""
for paragraph in document.paragraphs:
    prompt += paragraph.text + "\n"

@app.route('/send_message_to_bot', methods=['POST'])
def chat():
    print(f"Ricevuta richiesta da \"{request.remote_addr}\"")
    data = request.get_json()

    if not data or 'messages' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    messages = data['messages']
    print(f"{request.remote_addr}: {messages[-1]['content']}")
    messages.insert(0, {"role": "system", "content": prompt})
    try:
        full_response = ""
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
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
