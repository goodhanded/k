from typing import Protocol

class ClipboardProtocol(Protocol):
  def get(self) -> str:
    pass
  def set(self, content: str):
    pass