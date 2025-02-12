import unittest

from adapters.transcription.prompts.assimilation import assimilation_prompt


class TestAssimilationPrompt(unittest.TestCase):
    def test_empty_daily_note(self):
        transcript = "This is a test transcript."
        daily_note = ""
        prompt = assimilation_prompt(transcript, daily_note)
        self.assertIn("Transcripts for Today:", prompt)
        self.assertIn("There is no existing daily note content for today.", prompt)

    def test_existing_daily_note(self):
        transcript = "Another test transcript."
        daily_note = "Existing note content."
        prompt = assimilation_prompt(transcript, daily_note)
        self.assertIn("Here is the existing daily note content for today:", prompt)
        self.assertIn("Existing note content.", prompt)

if __name__ == '__main__':
    unittest.main()
