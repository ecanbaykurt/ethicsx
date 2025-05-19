import streamlit as st
import requests
from bs4 import BeautifulSoup

from agents.consent_agent import check_consent_violation
from agents.inference_agent import check_inferences
from agents.ethics_writer import generate_report
from agents.llm_agent import extract_consent_from_policy

st.set_page_config(page_title="EthixNet – LLM Audit", layout="centered")
st.title("🛡️ EthixNet – AI Data Ethics Watchdog (with Free LLM)")

input_method = st.radio("Choose Input Type", ["Paste Text", "Enter URL"])

text_input = ""
if input_method == "Paste Text":
    text_input = st.text_area("📄 Paste Privacy Policy or Terms Text", height=300)
elif input_method == "Enter URL":
    url = st.text_input("🌐 Enter Privacy Policy URL")
    if url:
        try:
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            text_input = soup.get_text()
            st.success("Website scraped successfully!")
        except Exception as e:
            st.error(f"Failed to fetch content: {e}")

if text_input:
    st.subheader("🤖 LLM-Suggested Consent Terms")
    consent_items = extract_consent_from_policy(text_input)
    st.markdown(f"`{', '.join(consent_items)}`")

    violations = check_consent_violation(consent_items, text_input)
    inferred = check_inferences(text_input)

    st.subheader("📋 EthixNet Report")
    if violations:
        st.error("❌ Consent Violations: " + ", ".join(violations))
    if inferred:
        st.warning("⚠️ Sensitive Inferences Detected: " + ", ".join(inferred))
    if not violations and not inferred:
        st.success("✅ No violations detected.")

    st.markdown("### 📜 Ethics Summary")
    st.code(generate_report("LiveInput", violations, inferred))
