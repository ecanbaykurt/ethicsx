import requests

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": "Bearer YOUR_HUGGINGFACE_API_KEY"}

def extract_consent_from_policy(text):
    prompt = (
        "Extract a comma-separated list of types of user data collected from this privacy policy:\n\n"
        + text[:1500]
    )
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        result = response.json()
        if isinstance(result, list):
            output = result[0].get("generated_text", "")
        else:
            output = result.get("generated_text", "")
        keywords = [kw.strip().lower() for kw in output.split(",") if kw.strip()]
        return keywords if keywords else ["email", "name", "location"]
    except Exception as e:
        print("LLM Error:", e)
        return ["email", "name", "location"]
