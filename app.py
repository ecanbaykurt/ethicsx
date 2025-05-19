import streamlit as st
import requests
from bs4 import BeautifulSoup

from agents.consent_agent import check_consent_violation
from agents.inference_agent import check_inferences
from agents.ethics_writer import generate_report

st.set_page_config(page_title="EthixNet - Live Text Audit", layout="centered")
st.title("🛡️ EthixNet – AI Data Ethics Watchdog (Text & URL)")
st.write("Paste a privacy policy, or enter a URL for live audit:")

input_method = st.radio("Choose Input Type", ["Paste Text", "Enter URL"])

text_input = ""
if input_method == "Paste Text":
    text_input = st.text_area("📄 Paste Privacy Policy or App Description Text", height=300)
elif input_method == "Enter URL":
    url = st.text_input("🌐 Enter URL")
    if url:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            text_input = soup.get_text()
            st.success("Website scraped successfully!")
        except Exception as e:
            st.error(f"Failed to fetch content: {e}")

if text_input:
    st.subheader("🧠 EthixNet Report")
    consent_claim = st.text_input("✍️ What was the declared consent? (comma-separated)", value="email, name, location")

    violations = check_consent_violation(consent_claim, text_input)
    inferred = check_inferences(text_input)

    if violations:
        st.error(f"❌ Consent Violations: {', '.join(violations)}")
    if inferred:
        st.warning(f"⚠️ Sensitive Inferences Detected: {', '.join(inferred)}")
    if not violations and not inferred:
        st.success("✅ No issues detected.")

    st.markdown("### 📜 Ethics Summary")
    st.code(generate_report("LiveInput", violations, inferred, None))
