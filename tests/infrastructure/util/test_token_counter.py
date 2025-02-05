import unittest
from infrastructure.util.token_counter import TokenCounter


class TestTokenCounter(unittest.TestCase):
    def test_count_tokens(self) -> None:
        tc = TokenCounter()
        text = "This is a test string"
        # Should split into 5 tokens
        count = tc.count_tokens(text)
        self.assertEqual(count, 5)


if __name__ == '__main__':
    unittest.main()
