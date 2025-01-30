import os
from application.intelligence import NoteVaultInterface
from domain.notes import Note
from domain.notes import NoteCollection
from domain.util.datetime import ym, date_string

class ObsidianVault(NoteVaultInterface):
  def __init__(self, path: str):
    self.path = path

  def save(self, note: Note, path: str):
    file_path = os.path.join(self.path, path)
    note.to_file(file_path)

  def get(self, path: str) -> Note:
    file_path = os.path.join(self.path, path)

    # If the file doesn't exist, create it
    if not os.path.exists(file_path):
      with open(file_path, 'w') as f:
        f.write('')

    return Note.from_path(file_path)

  def list(self, path: str) -> NoteCollection:
    path = os.path.join(self.path, path)
    return NoteCollection.from_path(path)

  def get_daily_note(self) -> Note:
    daily_note_file = f"{date_string()}.md"
    daily_note_path = os.path.join(self.path, 'Calendar', *ym(), daily_note_file)
    return self.get(daily_note_path)
  
  def get_all_notes(self) -> NoteCollection:
    return self.list('')

  def overwrite_daily_note(self, content: str):
    daily_note_file = f"{date_string()}.md"
    daily_note_path = os.path.join(self.path, 'Calendar', *ym(), daily_note_file)
    note = Note(content)
    self.save(note, daily_note_path)