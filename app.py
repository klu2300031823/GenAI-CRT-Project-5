import streamlit as st
import re
from PyPDF2 import PdfReader

st.set_page_config(
    page_title="Contract Review Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Contract Review Assistant")
st.write("Upload a contract and identify risky clauses, missing obligations, risk score, and recommendations.")

def extract_text(file):
    text = ""

    if file.name.endswith(".pdf"):
        pdf = PdfReader(file)

        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    else:
        text = file.read().decode("utf-8")

    return text


risk_patterns = {
    "Unlimited Liability": r"unlimited liability",
    "Auto Renewal": r"automatic renewal|auto renewal",
    "Termination Restriction": r"cannot terminate|non[- ]?cancellable",
    "Exclusive Agreement": r"exclusive rights|exclusive agreement",
    "Penalty Clause": r"penalty|liquidated damages",
    "Indemnification": r"indemnify|indemnification"
}

required_obligations = [
    "payment",
    "termination",
    "confidentiality",
    "governing law",
    "dispute resolution"
]

uploaded_file = st.file_uploader(
    "Upload Contract",
    type=["pdf", "txt"]
)

if uploaded_file:

    text = extract_text(uploaded_file)

    st.subheader("📃 Contract Content")

    st.text_area(
        "Extracted Text",
        text[:10000],
        height=250
    )

    risks = []

    for risk, pattern in risk_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            risks.append(risk)

    missing = []

    text_lower = text.lower()

    for item in required_obligations:
        if item not in text_lower:
            missing.append(item)

    risk_score = min(len(risks) * 15, 100)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚠ Risky Clauses")

        if risks:
            for risk in risks:
                st.error(risk)
        else:
            st.success("No risky clauses detected")

    with col2:
        st.subheader("📌 Missing Obligations")

        if missing:
            for item in missing:
                st.warning(item.title())
        else:
            st.success("No missing obligations detected")

    st.subheader("📊 Risk Score")

    st.progress(risk_score)

    st.metric(
        "Overall Risk Score",
        f"{risk_score}/100"
    )

    summary = f"""
Contract Review Summary

Risky Clauses Found: {len(risks)}
Missing Obligations: {len(missing)}

Risky Clauses:
{', '.join(risks) if risks else 'None'}

Missing Obligations:
{', '.join(missing) if missing else 'None'}

Recommendation:
Review flagged clauses before signing the agreement.
"""

    st.subheader("📝 Executive Summary")

    st.text_area(
        "Summary",
        summary,
        height=250
    )

    st.subheader("✅ Recommendations")

    if risks:
        st.write("• Review liability and indemnification clauses")
        st.write("• Verify renewal and termination conditions")
        st.write("• Consult legal team before approval")

    if missing:
        st.write("• Add missing legal obligations")
        st.write("• Include governing law section")
        st.write("• Include dispute resolution section")

    if not risks and not missing:
        st.success("Contract appears complete based on current checks.")
