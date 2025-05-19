SENSITIVE_KEYWORDS = ["mental health", "anxiety", "ethnicity", "sexual orientation", "religion"]

def check_inferences(data):
    return [kw for kw in SENSITIVE_KEYWORDS if kw in data.lower()]
