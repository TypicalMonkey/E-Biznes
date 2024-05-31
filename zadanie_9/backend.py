from flask import Flask, request, jsonify, render_template
import openai
import os
import requests

app = Flask(__name__)

# ukrycie kluca
openai.api_key = os.getenv("OPENAI_API_KEY")

#CORS
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt')
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )
        return jsonify({"response": response.choices[0].text.strip()})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    response = requests.post("http://localhost:5000/chat", json={'prompt': user_message})
    
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=8000, debug=True)
