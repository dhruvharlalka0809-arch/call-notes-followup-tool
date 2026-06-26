# Sales Follow-Up Automation Assistant

A Streamlit and CLI tool that turns messy sales call notes into a polished follow-up pack: call summary, email draft, and CRM note.

The app is designed for account executives, SDRs, founders, and business development teams who lose time after calls turning raw notes into clean next steps.

## What It Does

- Converts raw call notes or transcript snippets into a structured follow-up pack
- Produces a call summary, ready-to-edit email, and CRM note
- Preserves a strict no-invention rule for names, numbers, dates, and commitments
- Includes a deterministic preview mode so the public app works without an API key
- Supports Claude AI generation when `ANTHROPIC_API_KEY` is configured
- Saves downloadable follow-up files for handoff or CRM upload

## Why This Project Matters

This is a practical sales-ops automation workflow, not a toy prompt demo. It shows business process thinking, LLM prompt design, Streamlit deployment, input validation, and a safer fallback path for public reviewers.

## Tech Stack

- Python
- Streamlit
- Anthropic API, optional
- Standard-library tests with `unittest`

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app loads with sample notes by default, so it can be reviewed immediately.

## Optional AI Setup

Create a local `.env` file or add a Streamlit secret:

```bash
ANTHROPIC_API_KEY=your-api-key-here
```

Do not commit real API keys. `.env`, `.env.*`, `.en`, and Streamlit secrets are ignored.

## CLI Usage

Paste notes interactively:

```bash
python followup.py --name "Maria Gutierrez" --company "Brightpath Logistics"
```

Use the included sample:

```bash
python followup.py --file sample_notes.txt --name "Maria Gutierrez" --company "Brightpath Logistics"
```

Pipe notes in:

```bash
cat sample_notes.txt | python followup.py
```

## Validate

```bash
python -m unittest discover -s tests
```

Or run the full local validation script:

```bash
python scripts/validate.py
```

## Portfolio Talking Points

- Built a sales productivity workflow that reduces post-call admin work
- Designed a no-invention prompt for safer AI-generated sales communication
- Added fallback preview output so the deployed app remains usable without private credentials
- Added tests for prompt guardrails, file naming, and preview output structure

## Author

Dhruv Harlalka

MBA Finance, Middlesex University Dubai
