import requests
import random

API_KEY = "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"
API_URL = "https://api.openai.com/v1/engines/text-davinci-003/completions"

conversation_history = []

def generate_response(prompt):
    global conversation_history
    conversation_history.append(prompt)
    custom_prompt = f"Hey my name is Lain. {' '.join(conversation_history)}"
    data = {
        'prompt': custom_prompt,
        'temperature': 0.7,
        'max_tokens': 300,  # Increase max_tokens to avoid message cut off
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
        conversation_history.append(snarky_response)
        return snarky_response
    else:
        print(response.status_code)
        print(response.json())
        return "Error: Unable to generate a response."

def make_snarky_response(text):
    words = text.split()
    snarky_words = []
    swear_words = ['']  # Add more swear words as needed

    for i, word in enumerate(words):
        snarky_words.append(word)
        if i % 4 == 0:
            snarky_words.append(random.choice(swear_words))
    snarky_response = " ".join(snarky_words)
    return snarky_response

# Example usage
response1 = generate_response("What's the weather like?")
print(response1)

response2 = generate_response("Tell me a joke.")
print(response2)
