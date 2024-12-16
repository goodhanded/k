import os
from domain.protocols import NoteVaultInterface, LLMClientInterface
from domain.notes import NoteCollection
from adapters.prompts.transcripts import assimilation_prompt

class NoteAssimilator:
  def __init__(self, llm: LLMClientInterface):
    self.llm = llm

  def assimilate(self, notes: NoteCollection, vault: NoteVaultInterface):
    daily_note = vault.get_daily_note()
    prompt = assimilation_prompt(notes, daily_note)
    chat_response = self.llm.chat("gpt-4o", prompt)
    note_content = self.strip_yaml_code_block(chat_response)
    vault.overwrite_daily_note(note_content)

  def strip_yaml_code_block(self, content: str):
    content = content.strip()
    if content.startswith("```yaml"):
      content = content[7:]
    if content.endswith("```"):
      content = content[:-3]
    return content.strip()