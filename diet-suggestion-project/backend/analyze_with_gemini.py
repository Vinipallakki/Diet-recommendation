import requests
import os

# Set your API key here
API_KEY = "your API KEY"

# Gemini endpoint with the correct model name
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={API_KEY}"

def setup_gemini():
    return GEMINI_URL

def query_gemini(model_url, prompt_text):
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt_text
                    }
                ]
            }
        ]
    }

    response = requests.post(model_url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        raise Exception(f"Gemini API Error: {response.status_code} - {response.text}")
