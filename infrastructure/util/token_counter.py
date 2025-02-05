from application.util.token_counter_protocol import TokenCounterProtocol

class TokenCounter(TokenCounterProtocol):
    def count_tokens(self, text: str) -> int:
        return len(text.split())
