"""
followup.py — Call Notes -> Follow-Up Tool (v1)

Takes raw sales call notes (or a pasted transcript) and produces three things:
  1. Call Summary
  2. Follow-Up Email Draft
  3. CRM Note (structured fields)

The result is printed to the terminal AND saved to a text file named with
today's date and the prospect's name (e.g. output/2026-06-24_Jane-Doe.txt).

Usage:
    python3 followup.py                       # prompts you to paste notes
    python3 followup.py --name "Jane Doe" --company "Acme"
    python3 followup.py --file notes.txt      # read notes from a file
    cat notes.txt | python3 followup.py       # or pipe them in

Requires the ANTHROPIC_API_KEY environment variable to be set for AI generation.
"""

import argparse
import datetime
import os
import re
import sys

import anthropic

# The model we use for generation. Sonnet 4.6 balances cost and quality.
MODEL = "claude-sonnet-4-6"


def read_notes(file_path):
    """Get the raw call notes from a file, a pipe, or interactive paste."""
    # 1. Explicit --file wins.
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    # 2. If notes were piped in (e.g. `cat notes.txt | python3 followup.py`),
    #    stdin is not a terminal, so just read all of it.
    if not sys.stdin.isatty():
        return sys.stdin.read()

    # 3. Otherwise, prompt the user to paste and finish with Ctrl-D.
    print("Paste your call notes below.")
    print("When you're done, press Ctrl-D (on a new line) to finish.\n")
    return sys.stdin.read()


def build_prompt(notes, name, company, today):
    """Assemble the instruction we send to Claude.

    We pass today's date so the model can resolve relative dates like
    "follow up next Tuesday" and date the email correctly.
    """
    # Only mention the name/company hints if the rep actually provided them.
    hints = []
    if name:
        hints.append(f"Prospect name: {name}")
    if company:
        hints.append(f"Company name: {company}")
    hint_block = ("\n".join(hints) + "\n\n") if hints else ""

    return f"""You are a sales assistant. Today's date is {today}.

A sales rep will give you raw, possibly messy notes or a transcript from a
sales call. Turn it into exactly three sections, in this order, using these
markdown headings exactly:

## Call Summary
3-5 bullet points covering: what was discussed, the prospect's stated needs or
pain points, any objections raised, and who said they would do what next.

## Follow-Up Email Draft
A ready-to-send email the rep can send today with minimal editing. It MUST
reference at least two specific things that came up on the call, restate the
agreed next steps, and sound professional but warm (not robotic). Include a
subject line.
The email is held to the SAME no-invention rule as everything else:
- Do NOT state any specific year, number, statistic, or metric that is not in
  the notes (e.g. do not turn "2 years ago" into a specific year, and do not
  invent results like "90% adoption").
- Refer to events using only what the notes say (e.g. "your previous rollout",
  not a fabricated date).
- When mentioning attachments or collateral, describe them generally; do not
  invent figures or outcomes they supposedly contain.

## CRM Note
Fill in ALL of these five fields, one per line:
- Account/Company:
- Contact:
- Deal Stage Signal: (e.g. "interested", "needs budget approval", "competitor mentioned")
- Next Steps:
- Follow-Up Date: (resolve relative dates against today's date; use an actual date)

CRITICAL RULES:
- Use ONLY information that is actually present in the notes. Do NOT invent
  names, numbers, dates, commitments, or details that were not stated.
- If something needed for a field is not in the notes, write "not mentioned".

{hint_block}Here are the call notes:
---
{notes}
---"""


def generate(notes, name, company, today):
    """Send the notes to Claude and return the generated three-section text."""
    # The client automatically reads ANTHROPIC_API_KEY from the environment.
    client = anthropic.Anthropic()

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        messages=[
            {"role": "user", "content": build_prompt(notes, name, company, today)}
        ],
    )

    # A normal text answer is a single content block; .text is what we want.
    return response.content[0].text


def slugify(value):
    """Turn a prospect name into something safe for a file name.

    "Jane Doe" -> "Jane-Doe"; empty/unknown -> "unknown".
    """
    value = (value or "").strip()
    if not value:
        return "unknown"
    # Replace runs of anything that isn't a letter/number with a single dash.
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")
    return value or "unknown"


def save_output(text, name, today):
    """Save the result to output/<date>_<prospect>.txt and return the path."""
    os.makedirs("output", exist_ok=True)
    filename = f"{today}_{slugify(name)}.txt"
    path = os.path.join("output", filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def main():
    parser = argparse.ArgumentParser(
        description="Turn raw sales call notes into a summary, follow-up email, and CRM note."
    )
    parser.add_argument("--name", help="Prospect's name (optional).")
    parser.add_argument("--company", help="Company name (optional).")
    parser.add_argument("--file", help="Read notes from this file instead of pasting.")
    args = parser.parse_args()

    # Fail early with a friendly message if the key isn't set.
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY is not set in your environment.", file=sys.stderr)
        sys.exit(1)

    notes = read_notes(args.file)
    if not notes.strip():
        print("Error: no call notes were provided.", file=sys.stderr)
        sys.exit(1)

    today = datetime.date.today().isoformat()  # e.g. "2026-06-24"

    print("\nGenerating follow-up...\n")
    result = generate(notes, args.name, args.company, today)

    # Print to the terminal...
    print(result)

    # ...and save a copy for the rep to grab later.
    path = save_output(result, args.name, today)
    print(f"\n(Saved to {path})")


if __name__ == "__main__":
    main()
