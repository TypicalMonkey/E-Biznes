from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

backend_url = "http://localhost:5000/chat"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    response = requests.post(backend_url, json={'prompt': user_message})
    
    return jsonify(response.text)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
