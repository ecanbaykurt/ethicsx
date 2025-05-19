def generate_report(source, consent_violations, inferred_flags, bias=None):
    summary = f"Ethics Audit for: {source}\n"
    if consent_violations:
        summary += f"- Consent Violations: {', '.join(consent_violations)}\n"
    if inferred_flags:
        summary += f"- Inferred Traits Detected: {', '.join(inferred_flags)}\n"
    if bias:
        summary += f"- Bias Summary: {bias}\n"
    if not consent_violations and not inferred_flags and not bias:
        summary += "- No ethical risks detected.\n"
    return summary
