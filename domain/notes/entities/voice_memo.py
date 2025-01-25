from domain.filesystem import File

class VoiceMemo(File):
  def __init__(self, path: str):
    super().__init__(path)
    if not self.has_extension('.wav'):
      raise ValueError(f"Invalid file extension: {self.extension}")

  def accepted_extensions(self):
    return ['.wav']