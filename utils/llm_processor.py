# utils/llm_processor.py
import requests
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_filled_fields(template_text, report_text):
    prompt = f"""
    You are an insurance claims assistant. The following is an insurance form template with placeholders.
    Template:
    {template_text}

    And this is the photo report text:
    {report_text}

    Please extract values for each field in the template and return a JSON object with key-value pairs.
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",  # or another valid OpenRouter model
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

    try:
        json_response = response.json()
        return json.loads(json_response["choices"][0]["message"]["content"])
    except Exception as e:
        print("❌ Error from LLM API response:", response.text)
        raise ValueError("Failed to get valid response from LLM API. Check API key, model, or prompt.") from e
