import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {"Authorization": "Bearer YOUR_HUGGINGFACE_API_KEY"}

def extract_consent_from_policy(text):
    prompt = (
        "Extract a comma-separated list of user data types collected in this policy: "
        + text[:1500]
    )
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    try:
        result = response.json()
        output = result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "")
        return [kw.strip().lower() for kw in output.split(",") if kw.strip()]
    except:
        return ["email", "name", "location"]
