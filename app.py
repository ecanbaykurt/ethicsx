import streamlit as st
import pandas as pd

from agents.consent_agent import check_consent_violation
from agents.inference_agent import check_inferences
from agents.bias_agent import detect_bias
from agents.ethics_writer import generate_report

st.set_page_config(page_title="EthixNet - AI Ethics Watchdog", layout="wide")
st.title("🛡️ EthixNet: Multi-Agent AI Watchdog for Data Ethics")

uploaded = st.file_uploader("Upload your CSV or select demo", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = pd.read_csv("data/sample_input.csv")
    st.info("Using sample dataset.")

for idx, row in df.iterrows():
    st.subheader(f"🔍 Auditing: {row['Website']}")
    violations = check_consent_violation(row["User_Consent"], row["Actual_Data_Used"])
    inferred = check_inferences(row["Actual_Data_Used"])

    # Optional BiasAgent
    if "gender" in df.columns and "outcome" in df.columns:
        bias_summary = detect_bias(df)
    else:
        bias_summary = "Insufficient data for bias detection"

    report = generate_report(row["Website"], violations, inferred, bias_summary)
    st.markdown(report)

    if st.button(f"📄 Download Report for {row['Website']}", key=f"btn_{idx}"):
        with open(f"reports/{row['Website']}_ethics_report.txt", "w") as f:
            f.write(report)
        st.success(f"Saved to reports/{row['Website']}_ethics_report.txt")
