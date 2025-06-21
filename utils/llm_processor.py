# utils/llm_processor.py
import requests
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_filled_fields(template_text, extracted_text):
    prompt = f"""
You are an assistant that extracts relevant key-value pairs from an insurance photo report to fill out a DOCX template.

Template Fields:
{template_text}

Photo Report Content:
{extracted_text}

Return JSON of key-value mappings like:
{{"PolicyHolder": "John Doe", "Date": "2023-06-20", ...}}
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral",  # Or "deepseek-chat"
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]
