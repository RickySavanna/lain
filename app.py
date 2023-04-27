from flask import Flask, render_template, request, jsonify
from gpt3 import generate_response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chat')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    input_text = request.form['input']
    response_text = generate_response(input_text)
    return jsonify(response=response_text)

if __name__ == '__main__':
    app.run(debug=True)
