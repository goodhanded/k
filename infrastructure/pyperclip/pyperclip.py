import pyperclip

from application.filesystem import ClipboardProtocol

class Pyperclip(ClipboardProtocol):
  def get(self) -> str:
    return pyperclip.paste().strip()
  def set(self, content: str):
    pyperclip.copy(content)