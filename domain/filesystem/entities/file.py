import os

class File:
  def __init__(self, path: str):

    if not os.path.exists(path):
      raise FileNotFoundError(f"File not found: {path}")

    self.path = path
    self.name = os.path.basename(path)
    self.name_without_extension = os.path.splitext(self.name)[0]
    self.extension = os.path.splitext(self.name)[1]

  def has_extension(self, extension: str) -> bool:
    return self.extension == extension