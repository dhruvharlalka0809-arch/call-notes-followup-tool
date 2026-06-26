from __future__ import annotations

import re


def extract_signal_lines(notes: str, limit: int = 5) -> list[str]:
    lines = []
    for raw_line in notes.splitlines():
        line = raw_line.strip(" -\t")
        if not line:
            continue
        if len(line) < 12:
            continue
        lines.append(line)
    return lines[:limit]


def infer_follow_up_date(notes: str) -> str:
    lower_notes = notes.lower()
    if "after the 4th of july" in lower_notes or "after july 4" in lower_notes:
        return "after July 4"
    if "next week" in lower_notes:
        return "next week"
    if "tomorrow" in lower_notes:
        return "tomorrow"
    return "not mentioned"


def infer_stage_signal(notes: str) -> str:
    lower_notes = notes.lower()
    signals = []
    if "competitor" in lower_notes or "talking to" in lower_notes:
        signals.append("competitor mentioned")
    if "budget" in lower_notes or "sign off" in lower_notes or "approval" in lower_notes:
        signals.append("needs budget approval")
    if "liked" in lower_notes or "engaged" in lower_notes or "interested" in lower_notes:
        signals.append("interested")
    return ", ".join(signals) if signals else "not mentioned"


def clean_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return text
    return text[0].upper() + text[1:]


def build_preview_followup(notes: str, name: str | None, company: str | None, today: str) -> str:
    signal_lines = extract_signal_lines(notes)
    first_detail = clean_sentence(signal_lines[0]) if signal_lines else "Thank you for the conversation today."
    second_detail = clean_sentence(signal_lines[1]) if len(signal_lines) > 1 else "I appreciated learning more about your current priorities."
    account = company or "not mentioned"
    contact = name or "not mentioned"
    follow_up_date = infer_follow_up_date(notes)
    stage_signal = infer_stage_signal(notes)
    summary = "\n".join(f"- {clean_sentence(line)}" for line in signal_lines) or "- not mentioned"

    return f"""## Call Summary
{summary}

## Follow-Up Email Draft
Subject: Follow-up from today's call

Hi {name or "there"},

Thank you for taking the time to speak today. I noted that {first_detail.lower()} I also captured that {second_detail.lower()}

As discussed, I will follow up with the relevant materials and next steps so the team can evaluate fit clearly.

Best,
Dhruv

## CRM Note
- Account/Company: {account}
- Contact: {contact}
- Deal Stage Signal: {stage_signal}
- Next Steps: send follow-up materials and confirm the next conversation
- Follow-Up Date: {follow_up_date}

Generated on: {today}
"""
