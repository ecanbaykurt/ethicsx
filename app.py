import streamlit as st
import requests
from bs4 import BeautifulSoup

# Import agents
from agents.consent_agent import check_consent_violation
from agents.inference_agent import check_inferences
from agents.ethics_writer import generate_report
from agents.llm_agent import extract_consent_from_policy
from agents.autogen_agent import analyze_ethics_summary  # MetaPrompt version, no API needed

# Page config
st.set_page_config(page_title="EthixNet – AI Ethics Inspector", layout="centered")
st.title("🛡️ EthixNet – Multi-Agent AI Watchdog (LLM + AutoGen)")
st.caption("Audit any website or policy for consent risks, profiling, and ethics violations.")

# Input type
input_method = st.radio("📥 Choose Input Method", ["Paste Text", "Enter URL"])
text_input = ""

# Text or URL input
if input_method == "Paste Text":
    text_input = st.text_area("📄 Paste policy, description, or terms text:", height=300)
else:
    url = st.text_input("🌐 Enter a public webpage or privacy policy URL")
    if url:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            text_input = soup.get_text()
            st.success("✅ Website scraped successfully!")
        except Exception as e:
            st.error(f"⚠️ Failed to fetch content: {e}")

# Run analysis if input exists
if text_input:
    st.divider()
    st.subheader("🤖 Step 1: LLM-Suggested Consent Terms")
    consent_items = extract_consent_from_policy(text_input)
    st.markdown(f"`{', '.join(consent_items)}`")

    st.subheader("🧠 Step 2: Violation & Inference Detection")
    violations = check_consent_violation(consent_items, text_input)
    inferred = check_inferences(text_input)

    if violations:
        st.error(f"❌ Consent Violations: {', '.join(violations)}")
    if inferred:
        st.warning(f"⚠️ Sensitive Inferences Detected: {', '.join(inferred)}")
    if not violations and not inferred:
        st.success("✅ No ethical risks or inferences detected.")

    st.subheader("📜 Step 3: Ethics Summary Report")
    st.code(generate_report("LiveInput", violations, inferred))

    st.subheader("🧾 Step 4: AutoGenAgent Ethical Brief (MetaPrompt)")
    paragraph = analyze_ethics_summary(text_input)
    st.write(paragraph)

    st.divider()
    st.caption("Built with ❤️ by EthixNet — bringing transparency to AI systems.")
