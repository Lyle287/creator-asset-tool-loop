import unittest
from unittest.mock import patch

from types import SimpleNamespace

from creator_workflow import ProcessingResult, next_actions
from creator_agent import ask_for_actions


class CreatorWorkflowTest(unittest.TestCase):
    def test_processed_asset_reaches_subscribers(self) -> None:
        result = ProcessingResult("studio-cut.mp4", True, 12)
        self.assertEqual(next_actions(result), ["deliver_asset", "notify_subscribers"])

    def test_unprocessed_asset_stays_in_review(self) -> None:
        result = ProcessingResult("studio-cut.mp4", False, 12)
        self.assertEqual(next_actions(result), ["review_content"])

    @patch("creator_agent.OpenAI")
    def test_string_false_from_model_stays_in_review(self, openai_class) -> None:
        openai_class.return_value.chat.completions.create.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content='{"processed": "false", "subscriber_count": 12}'))]
        )
        self.assertEqual(ask_for_actions("studio-cut.mp4", "ready"), ["review_content"])


if __name__ == "__main__":
    unittest.main()
