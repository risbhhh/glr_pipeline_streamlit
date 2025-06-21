import os
import requests
import json

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # This is pulled from Streamlit secrets

def get_filled_fields(template_text, report_text):
    prompt = f"""
You are an insurance assistant. The following is a template and a photo report. 
Extract and match fields from the report to fill the template as key-value pairs in JSON format.

TEMPLATE:
{template_text}

REPORT:
{report_text}

Return only a valid JSON object like:
{{
    "Name": "John Doe",
    "PolicyNumber": "123456",
    ...
}}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",  # You can try "openai/gpt-3.5-turbo" if available
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        json_response = response.json()

        # Log raw response to help with debugging in logs
        print("LLM response text:", json_response)

        message_content = json_response.get("choices", [{}])[0].get("message", {}).get("content", "")
        return json.loads(message_content)  # Assumes response is valid JSON string
    except Exception as e:
        print("❌ Error communicating with OpenRouter API:", e)
        print("❌ Full response text (if any):", response.text if response else "No response")
        return {}  # Return empty dict so app doesn't crash
