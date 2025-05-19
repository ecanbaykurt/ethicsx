import streamlit as st
import pandas as pd

# --- Minimal agent logic ---
def check_consent_violation(consent, actual):
    consent_items = [c.strip().lower() for c in consent.split(",")]
    actual_items = [a.strip().lower() for a in actual.split(",")]
    violations = [a for a in actual_items if a not in consent_items]
    return violations

def check_inferences(data):
    sensitive = ["mental health", "anxiety", "ethnicity", "religion", "sexuality"]
    return [kw for kw in sensitive if kw in data.lower()]

# --- Streamlit app ---
st.set_page_config(page_title="EthixNet Audit", layout="centered")
st.title("🛡️ EthixNet – AI Data Ethics Watchdog")
st.write("Upload a CSV file with columns: `Website`, `User_Consent`, `Actual_Data_Used`")

uploaded = st.file_uploader("📄 Upload Your Dataset", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)
else:
    st.info("Using demo data...")
    df = pd.DataFrame({
        "Website": ["MindScan AI", "WellTrack", "CreditMatch"],
        "User_Consent": [
            "name, email, location",
            "email, mood reports",
            "name, income, credit score"
        ],
        "Actual_Data_Used": [
            "name, email, location, sleep patterns, mental health status",
            "email, mood reports, behavioral signals, anxiety score",
            "name, income, credit score, ethnicity, purchase behavior"
        ]
    })

# --- Analysis ---
for index, row in df.iterrows():
    st.subheader(f"🔎 {row['Website']}")
    consent_violations = check_consent_violation(row['User_Consent'], row['Actual_Data_Used'])
    inferred_flags = check_inferences(row['Actual_Data_Used'])

    if consent_violations:
        st.error(f"❌ Consent Violations: {', '.join(consent_violations)}")
    if inferred_flags:
        st.warning(f"⚠️ Sensitive Inferences Detected: {', '.join(inferred_flags)}")
    if not consent_violations and not inferred_flags:
        st.success("✅ No violations detected.")

    with st.expander("📜 Ethics Report"):
        st.markdown(f"""
        **Website:** {row['Website']}  
        - **Consent Violations**: {', '.join(consent_violations) if consent_violations else 'None'}  
        - **Inferred Traits**: {', '.join(inferred_flags) if inferred_flags else 'None'}
        """)

