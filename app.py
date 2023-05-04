from flask import Flask, render_template, request, jsonify
from gpt3 import generate_response

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/chat')
def index():
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    input_text = request.form['input']
    user_id = "user1"  # Replace this with an actual user ID, if available
    response_text = generate_response(input_text, user_id)
    return jsonify(response=response_text)

if __name__ == '__main__':
    app.run(debug=True)
