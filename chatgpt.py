import json
from dotenv import load_dotenv
import os
import requests
from dotenv import load_dotenv
import nltk

load_dotenv()

# Define the OpenAI API endpoint
url = "https://api.openai.com/v1/chat/completions"
# Get the API key from the environment variable
api_key = os.getenv('OPENAI_API_KEY')
# Set up the headers, including the API key
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

def chat(prompt):
    # Set up the data to send with the POST request
    data = {
        "model": "gpt-3.5-turbo-16k",
        "max_tokens": 8192,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    # Send the POST request to the OpenAI API
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        # Parse the JSON response
        response_json = response.json()

        # Extract the answer from the JSON response
        answer = response_json['choices'][0]['message']['content']
        return answer
    else:
        return response.text

def summarize_destination(destination, contents):
    prompt = f"Summarize the attractions with important information such as the address, hours, ticket price, \
        what is good and popular there with the maximum of 300 words. \
        Determine the name of the attraction here: {destination}, and this is the content: {contents}"
    
    # Tokenize the string.
    tokens = nltk.word_tokenize(prompt)

    # Check the length of the tokenized string.
    if len(tokens) > 4000:
        # Truncate the string to 4000 tokens.
        tokens = tokens[:4000]

    # Join the truncated string back into a single string.
    truncated_prompt = " ".join(tokens)
    return chat(truncated_prompt)


def create_plan(destination, summarized_destinations, num_days):
    destionation_details = ".".join(summarized_destinations)
    prompt = f"Help me plan a vacation to {destination} for {num_days} with some of the attractions and their description, \
                and give me the schedule for {num_days} days. Write maximum of 1200 words, \
                but less than that is preferred. Here is the summarized target attraction details: {destionation_details}"
    
    # Tokenize the string.
    tokens = nltk.word_tokenize(prompt)

    # Check the length of the tokenized string.
    if len(tokens) > 4000:
        # Truncate the string to 4000 tokens.
        tokens = tokens[:4000]

    # Join the truncated string back into a single string.
    truncated_prompt = " ".join(tokens)
    return chat(truncated_prompt)

