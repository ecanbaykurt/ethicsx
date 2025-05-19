SENSITIVE_KEYWORDS = [
    "mental health", "anxiety", "ethnicity",
    "sexual orientation", "religion", "disability", "political view"
]

def check_inferences(data):
    return [kw for kw in SENSITIVE_KEYWORDS if kw in data.lower()]
