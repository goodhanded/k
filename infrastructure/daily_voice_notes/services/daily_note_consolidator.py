import os
from application.intelligence import LLMClientProtocol
from application.notes import NoteVaultProtocol
from application.daily_voice_notes import DocumentConsolidatorProtocol
from domain.filesystem import Document, DocumentCollection
from adapters.transcription import assimilation_prompt

class DailyNoteConsolidator(DocumentConsolidatorProtocol):
    def __init__(self, llm: LLMClientProtocol, note_vault: NoteVaultProtocol):
        self.llm = llm
        self.note_vault = note_vault

    def consolidate(self, documents: DocumentCollection):
        daily_note = self.note_vault.get_daily_note()
        prompt = assimilation_prompt(documents.to_document().content, daily_note.content)
        chat_response = self.llm.chat("gpt-4o", prompt)
        note_content = self._strip_yaml_code_block(chat_response)
        self.note_vault.overwrite_daily_note(note_content)

    def _strip_yaml_code_block(self, content: str):
        content = content.strip()
        if content.startswith("```yaml"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        return content.strip()