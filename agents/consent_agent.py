KNOWN_DATA_TYPES = ["email", "name", "location", "mood", "health", "ethnicity", "income", "face", "gps", "contact", "voice", "messages"]

def check_consent_violation(consent_items, text):
    return [item for item in KNOWN_DATA_TYPES if item in text.lower() and item not in consent_items]
