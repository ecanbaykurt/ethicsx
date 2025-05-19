def analyze_ethics_summary(text):
    """
    Simulates a MetaPrompt-style ethics summary without external API.
    You can later swap this with an LLM call if desired.
    """
    meta_prompt = """
You are an AI Ethics Inspector. Analyze the following text and describe:
- Any signs of unethical behavior
- Privacy or data collection risks
- Scam or manipulative patterns
- Use of sensitive language
- Sarcasm, dark patterns, or coercion

Return a short professional paragraph summarizing your concerns.
"""

    summary = meta_prompt + "\n\n---\n\n" + text[:2000]
    
    # Fallback template
    if any(keyword in text.lower() for keyword in ["location", "mood", "income", "mental", "religion"]):
        return (
            "This content reveals multiple privacy-sensitive elements such as mood, income, and religion without clear user consent. "
            "It suggests potential profiling behavior, and may contain indicators of emotional inference or discriminatory risk. "
            "There is no visible compliance structure ensuring ethical data handling or transparency."
        )
    else:
        return (
            "No immediate unethical signals detected. The content appears informational. "
            "No personally identifiable data or profiling behavior is observed based on the scanned text."
        )
