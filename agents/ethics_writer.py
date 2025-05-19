def generate_report(site, consent_violations, inferred_flags, bias_report):
    summary = f"🔍 Ethics Audit for: **{site}**\n\n"
    if consent_violations:
        summary += f"- ❌ Consent Violations: {', '.join(consent_violations)}\n"
    if inferred_flags:
        summary += f"- ⚠️ Inferred Traits Detected: {', '.join(inferred_flags)}\n"
    if bias_report and bias_report != "Insufficient data for bias detection":
        summary += f"- ⚖️ Bias Summary:\n{bias_report}\n"
    return summary or "✅ No violations detected."
