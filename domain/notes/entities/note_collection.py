import os

from domain.notes import Note

class NoteCollection:
  notes: list[Note]
  content: str

  def __init__(self, notes: list[Note]):
    self.notes = notes
    self.content = '\n\n'.join([note.content for note in notes]) if notes else ''

  def add(self, note: Note):
    self.notes.append(note)

  def remove(self, note: Note):
    self.notes.remove(note)

  def from_path(path: str) -> 'NoteCollection':
    notes = []
    for file_name in os.listdir(path):
      # Ignore dot files or hidden files
      if file_name.startswith('.'):
        continue
      print(file_name)
      file_path = os.path.join(path, file_name)
      print(file_path)
      note = Note.from_path(file_path)
      notes.append(note)
      collection = NoteCollection(notes)
    return collection

  def __iter__(self):
    return iter(self.notes)

  def __len__(self):
    return len(self.notes)