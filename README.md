# Call Notes → Follow-Up Tool (v1)

A command-line tool that turns raw sales call notes (or a pasted transcript)
into three things, right after the call ends:

1. **Call Summary** — the key points, needs, objections, and next steps
2. **Follow-Up Email Draft** — ready to send with minimal editing
3. **CRM Note** — structured fields you copy into your CRM

It prints the result to your terminal **and** saves a copy to
`output/<date>_<prospect-name>.txt`.

## Setup

You need Python 3 and the Anthropic SDK:

```bash
pip install anthropic
```

Your Claude API key must be available as an environment variable:

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

(It's already set in this environment.)

## Usage

Run it and paste your notes when prompted, then press **Ctrl-D** to finish:

```bash
python3 followup.py
```

Optionally pass the prospect and company so they're always filled in:

```bash
python3 followup.py --name "Maria Gutierrez" --company "Brightpath Logistics"
```

Read notes from a file instead of pasting:

```bash
python3 followup.py --file sample_notes.txt
```

Or pipe notes straight in:

```bash
cat sample_notes.txt | python3 followup.py
```

## Try it

A realistic example is included:

```bash
python3 followup.py --file sample_notes.txt --name "Maria Gutierrez" --company "Brightpath Logistics"
```

## What v1 does NOT do

No CRM integration, no audio transcription, no email sending, no stored
history, no team features. It generates text you copy in manually.

## The model

This tool uses Claude Sonnet 4.6 (`claude-sonnet-4-6`) — a strong balance of
quality and cost. To switch models, edit the `MODEL` constant at the top of
`followup.py`.
