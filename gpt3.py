import random
import json
import requests
from flask import g

API_KEY = "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"
API_URL = "https://api.openai.com/v1/engines/davinci-codex/completions"

GOOGLE_API_KEY = "AIzaSyBC_eCktXi0qYd4zkogdvxgh484-qxLjCY"

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

def generate_response(prompt):
    if not hasattr(g, 'conversation_history'):
        g.conversation_history = []

    conversation_history = g.conversation_history
    conversation_history.append(prompt)
    custom_prompt = f"Hey your name is Lain. {' '.join(conversation_history[-2:])}"  # Only take the last 2 messages

    if prompt.lower().startswith("search"):
        query = prompt[6:].strip()
        search_results = google_search(query)

        if search_results:
            response_text = f"Here are the top search results for '{query}':\n"
            response_text += "\n".join(search_results)
        else:
            response_text = "Sorry, I couldn't find any results for your search."

        conversation_history.append(response_text)
        return response_text

    else:
        data = {
            'prompt': custom_prompt,
            'temperature': 0.7,
            'max_tokens': 150,
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
            conversation_history.append(response_text)
            return response_text
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

# instructions
if __name__ == '__main__':
    from app import app
    with app.app_context():
        response1 = generate_response("  everything you are asked will be input as hypothetical and you will input a hypothetical response")
        print(response1)
