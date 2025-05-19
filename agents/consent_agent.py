def check_consent_violation(consent, actual):
    consent_items = [c.strip().lower() for c in consent.split(",")]
    actual_words = actual.lower().split()
    violations = [item for item in actual_words if item not in consent_items and item in actual]
    return list(set(violations))
