import unittest

from followup import build_prompt, slugify
from followup_preview import build_preview_followup, infer_stage_signal


class FollowupToolTests(unittest.TestCase):
    def test_slugify_handles_empty_and_symbols(self):
        self.assertEqual(slugify("Maria Gutierrez"), "Maria-Gutierrez")
        self.assertEqual(slugify(""), "unknown")
        self.assertEqual(slugify("A/B Test"), "A-B-Test")

    def test_prompt_enforces_no_invention_rule(self):
        prompt = build_prompt("asked for ROI deck", "Maria", "Brightpath", "2026-06-27")

        self.assertIn("Use ONLY information", prompt)
        self.assertIn("Do NOT invent", prompt)
        self.assertIn("Follow-Up Date", prompt)

    def test_preview_generates_required_sections(self):
        result = build_preview_followup(
            "liked the demo\nneeds budget approval\ncompetitor mentioned",
            "Maria",
            "Brightpath",
            "2026-06-27",
        )

        self.assertIn("## Call Summary", result)
        self.assertIn("## Follow-Up Email Draft", result)
        self.assertIn("## CRM Note", result)

    def test_stage_signal_combines_recruiter_relevant_buying_signals(self):
        signal = infer_stage_signal("liked demo, competitor mentioned, needs Trevor sign off")

        self.assertIn("competitor mentioned", signal)
        self.assertIn("needs budget approval", signal)
        self.assertIn("interested", signal)


if __name__ == "__main__":
    unittest.main()
