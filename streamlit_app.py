import datetime
import os

import streamlit as st

from followup import generate, slugify
from followup_preview import build_preview_followup


st.set_page_config(
    page_title="Sales Follow-Up Automation Assistant",
    page_icon=":telephone_receiver:",
    layout="wide",
)


@st.cache_data
def load_sample_notes() -> str:
    with open("sample_notes.txt", "r", encoding="utf-8") as file:
        return file.read()


def get_api_key() -> str | None:
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except (KeyError, FileNotFoundError):
        return os.environ.get("ANTHROPIC_API_KEY")


st.title("Sales Follow-Up Automation Assistant")
st.caption("Convert messy call notes into a call summary, follow-up email, and CRM note.")

api_key = get_api_key()
if api_key:
    os.environ["ANTHROPIC_API_KEY"] = api_key
else:
    st.info("AI generation is disabled until ANTHROPIC_API_KEY is configured. You can still preview the workflow with the deterministic draft.")

with st.sidebar:
    st.header("Output Pack")
    st.write("Call summary")
    st.write("Follow-up email")
    st.write("CRM note")
    mode = st.radio("Generation mode", ["Preview draft", "Claude AI"], disabled=not bool(api_key))
    use_sample = st.toggle("Use sample call notes", value=True)

default_notes = load_sample_notes() if use_sample else ""

with st.form("input_form"):
    notes = st.text_area(
        "Call notes or transcript",
        value=default_notes,
        height=280,
        placeholder="Paste raw sales call notes, discovery notes, or transcript snippets.",
    )

    col1, col2 = st.columns(2)
    with col1:
        prospect_name = st.text_input("Prospect name", value="Maria Gutierrez" if use_sample else "")
    with col2:
        company_name = st.text_input("Company name", value="Brightpath Logistics" if use_sample else "")

    submitted = st.form_submit_button("Generate Follow-Up")

if submitted:
    if not notes.strip():
        st.warning("Paste call notes before generating.")
        st.stop()

    today = datetime.date.today().isoformat()
    if mode == "Claude AI":
        with st.spinner("Generating AI follow-up pack..."):
            result = generate(notes, prospect_name or None, company_name or None, today)
    else:
        result = build_preview_followup(notes, prospect_name or None, company_name or None, today)

    left, right = st.columns([2, 1])
    with left:
        st.markdown(result)
    with right:
        st.subheader("Workflow Value")
        st.write("Saves post-call admin time")
        st.write("Standardizes CRM notes")
        st.write("Reduces missed follow-up details")
        st.write("Keeps the rep in control before sending")

    filename = f"{today}_{slugify(prospect_name)}.txt"
    st.download_button(
        label="Download follow-up pack",
        data=result,
        file_name=filename,
        mime="text/plain",
    )
else:
    st.subheader("Sample Workflow")
    st.markdown(build_preview_followup(default_notes, "Maria Gutierrez", "Brightpath Logistics", datetime.date.today().isoformat()))
