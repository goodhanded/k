import os

from application.notes import NoteVaultProtocol
from domain.filesystem import Document, DocumentCollection
from infrastructure.util import DatetimeService
from application.config import ConfigProtocol


class ObsidianVault(NoteVaultProtocol):
    def __init__(self, path: str, config: ConfigProtocol):
        self.path = path
        self.config = config
        self.datetime_service = DatetimeService()

    def save(self, document: Document, path: str):
        file_path = os.path.join(self.path, path)
        document.to_file(file_path)

    def get(self, path: str) -> Document:
        if not path.endswith('.md'):
            path = f"{path}.md"
        file_path = os.path.join(self.path, path)
        
        # If the file doesn't exist, create it
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write('')

        return Document.from_path(file_path)

    def list(self, path: str) -> DocumentCollection:
        path = os.path.join(self.path, path)
        return DocumentCollection.from_path(path)

    def get_daily_note(self) -> Document:
        daily_note_file = f"{self.datetime_service.date_string()}.md"
        calendar_folder = self.config.get("OBSIDIAN_CALENDAR_FOLDER", "Calendar")
        daily_note_path = os.path.join(self.path, calendar_folder, *self.datetime_service.ym(), daily_note_file)
        return self.get(daily_note_path)

    def get_all_notes(self) -> DocumentCollection:
        return self.list('')

    def overwrite_daily_note(self, content: str):
        daily_note_file = f"{self.datetime_service.date_string()}.md"
        calendar_folder = self.config.get("OBSIDIAN_CALENDAR_FOLDER", "Calendar")
        daily_note_path = os.path.join(self.path, calendar_folder, *self.datetime_service.ym(), daily_note_file)
        note = Document(content)
        self.save(note, daily_note_path)
