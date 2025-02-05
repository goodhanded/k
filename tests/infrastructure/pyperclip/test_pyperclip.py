import unittest
from unittest.mock import patch
from infrastructure.pyperclip.pyperclip import Pyperclip


class TestPyperclip(unittest.TestCase):
    def test_copy_and_paste(self):
        # Patch the underlying pyperclip methods
        with patch('infrastructure.pyperclip.pyperclip.pyperclip.copy') as mock_copy, \
             patch('infrastructure.pyperclip.pyperclip.pyperclip.paste', return_value="mocked content") as mock_paste:
            clip = Pyperclip()
            clip.set("any content")
            result = clip.get()
            mock_copy.assert_called_once_with("any content")
            self.assertEqual(result, "mocked content")


if __name__ == '__main__':
    unittest.main()
