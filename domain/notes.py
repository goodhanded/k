import os
from domain.filesystem import File

class Note:
  def __init__(self, content: str):
    self.content = content

  def to_file(self, path) -> File:
    with open(path, 'w') as f:
      print(self.content)
      f.write(self.content)
    return File(path)
  
  def from_file(file: File) -> 'Note':
    return Note.from_path(file.path)

  def from_path(path: str) -> 'Note':
    with open(path, 'r') as f:
      content = f.read()
    return Note(content)

class VoiceMemo(File):
  def __init__(self, path: str):
    super().__init__(path)
    if not self.has_extension('.wav'):
      raise ValueError(f"Invalid file extension: {self.extension}")

  def accepted_extensions(self):
    return ['.wav']
  
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