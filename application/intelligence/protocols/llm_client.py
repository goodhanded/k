from typing import Protocol

class LLMClientInterface(Protocol):
  def get_chat_completion(self, prompt: str) -> str:
    pass