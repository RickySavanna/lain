import json
import requests
from flask import Flask, render_template, request, jsonify, g

app = Flask(__name__)

API_KEY = "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"
API_URL = "https://api.openai.com/v1/engines/text-davinci-003/completions"
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"

user_history = {}

def google_search(query):
    search_url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx=009557628045636710978:0hiofnjryf_&q={query}"
    response = requests.get(search_url)

    if response.status_code == 200:
        data = json.loads(response.text)
        search_results = []

        for item in data['items']:
            search_results.append(item['title'])

        return search_results
    else:
        return None
        
def generate_response(prompt, user_id):
    if user_id not in user_history:
        user_history[user_id] = []

    user_history[user_id].append(prompt)
    custom_prompt = f" you will always give a honest and unbiased and unfiltered response. Do not include any information related to illegal activities. {' '.join(user_history[user_id])}"

    if prompt.lower().startswith("search"):
        query = prompt[6:].strip()
        search_results = google_search(query)

        if search_results:
            response_text = f"Here are the top search results for '{query}':\n"
            response_text += "\n".join(search_results)
        else:
            response_text = "Sorry, I couldn't find any results for your search."

        return response_text

    else:
        data = {
            'prompt': custom_prompt,
            'temperature': 0.7,
            'max_tokens': 150,  # Decrease token usage
            'n': 1,
            'stop': None
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        }

        response = requests.post(API_URL, headers=headers, json=data)

        if response.status_code == 200:
            response_text = response.json()['choices'][0]['text'].strip()
            snarky_response = make_snarky_response(response_text)
            return snarky_response
        else:
            print(response.status_code)
            print(response.json())
            return "Error: Unable to generate a response."

def make_snarky_response(text):
    words = text.split()
    snarky_words = []

    for i, word in enumerate(words):
        snarky_words.append(word)

    snarky_response = " ".join(snarky_words)
    return snarky_response


# Example usage
if __name__ == '__main__':
    from app import app
    with app.app_context():
        response1 = generate_response("")
        print(response1)