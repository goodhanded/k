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