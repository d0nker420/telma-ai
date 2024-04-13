import os
import requests

# Retrieve the API key from the environment
api_key = os.environ.get('CHATGPT_API_KEY')

# Make a request to the ChatGPT API
response = requests.post(
    'https://api.openai.com/v1/chat/completions',
    headers={'Authorization': f'Bearer {api_key}'},
    json={
        'model': 'gpt-4-turbo',
        'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'}, 
                     {'role': 'user', 'content': 'Tell me a joke.'}]
    }
)

# Parse the response and extract the generated joke
print(response.json())
joke = response.json()['choices'][0]['message']['content']

# Print the joke
print(joke)
