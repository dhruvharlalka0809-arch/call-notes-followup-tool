"""
streamlit_app.py — Web UI for the Call Notes → Follow-Up Tool

Run locally:
    streamlit run streamlit_app.py

For deployment, set ANTHROPIC_API_KEY in Streamlit secrets or the environment.
"""

import datetime
import os

import streamlit as st

from followup import generate, slugify

st.set_page_config(page_title="Call Follow-Up Generator", page_icon="📞")

st.title("Call Follow-Up Generator")
st.markdown(
    "Paste your sales call notes below and get a **call summary**, "
    "**follow-up email draft**, and **CRM note** in seconds."
)

# --- API key ----------------------------------------------------------------
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except (KeyError, FileNotFoundError):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    st.error(
        "**ANTHROPIC_API_KEY** is not configured. "
        "Set it in `.streamlit/secrets.toml` or as an environment variable."
    )
    st.stop()

os.environ["ANTHROPIC_API_KEY"] = api_key

# --- Input form --------------------------------------------------------------
with st.form("input_form"):
    notes = st.text_area(
        "Call notes",
        height=250,
        placeholder="Paste your raw call notes or transcript here…",
    )

    col1, col2 = st.columns(2)
    with col1:
        prospect_name = st.text_input("Prospect name (optional)")
    with col2:
        company_name = st.text_input("Company name (optional)")

    submitted = st.form_submit_button("Generate Follow-Up")

# --- Generate & display -------------------------------------------------------
if submitted:
    if not notes.strip():
        st.warning("Please paste some call notes before generating.")
        st.stop()

    today = datetime.date.today().isoformat()

    with st.spinner("Generating follow-up…"):
        result = generate(notes, prospect_name or None, company_name or None, today)

    st.markdown(result)

    filename = f"{today}_{slugify(prospect_name)}.txt"
    st.download_button(
        label="Download as text file",
        data=result,
        file_name=filename,
        mime="text/plain",
    )
