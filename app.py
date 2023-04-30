from flask import Flask, render_template, request, jsonify, g
from gpt3 import generate_response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chat')
def index():
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    input_text = request.form['input']
    response_text = generate_response(input_text)
    return jsonify(response=response_text)

@app.before_request
def before_request():
    if not hasattr(g, 'conversation_history'):
        g.conversation_history = []


if __name__ == '__main__':
    app.run(debug=True)
