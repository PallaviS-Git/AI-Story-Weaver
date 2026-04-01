# story_manager.py
import os
import requests
from prompts import STORY_SYSTEM_PROMPT
from dotenv import load_dotenv
import time

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.ai/v1/llm"

def call_groq_api(prompt, temperature=0.7, max_tokens=400):
    """
    Call Groq LLM with the prompt and handle rate limits.
    """
    headers = {"Authorization": f"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"}
    payload = {
        "prompt": prompt,
        "temperature": temperature,
        "max_output_tokens": max_tokens
    }

    for attempt in range(3):  # Retry logic for rate limits
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 429:
            wait = 2 ** attempt
            print(f"Rate limit hit. Retrying in {wait}s...")
            time.sleep(wait)
            continue
        elif response.status_code != 200:
            raise Exception(f"API Error: {response.text}")
        return response.json()["output_text"]
    raise Exception("Failed after multiple retries due to rate limit.")