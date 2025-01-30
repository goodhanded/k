import os
from typing import List
from ..enums.ext import Ext

class File:
  """
  Represents a file in the filesystem

  Attributes:
    - path: The full path to the file
    - name: The name of the file
    - name_without_extension: The name of the file without the extension
    - extension: The file extension
  """
  def __init__(self, path: str):
    """
    Initializes a new instance of the File class

    Arguments:
      - path: The full path to the file
    """

    if not os.path.exists(path):
      raise FileNotFoundError(f"File not found: {path}")

    self.path = path
    self.name = os.path.basename(path)
    self.name_without_extension = os.path.splitext(self.name)[0]
    self.extension = os.path.splitext(self.name)[1]

    cls = self.__class__
    if cls.required_extensions() and self.extension.lower().lstrip('.') not in [ext.name.lower() for ext in cls.required_extensions()]:
      raise ValueError(f"Invalid extension: {self.extension} for {cls.__name__}. Expected: {cls.required_extensions()}")

  def has_extension(self, extension: str) -> bool:
    """
    Returns True if the file has the specified extension

    Arguments:
      - extension: The extension to check for
    """
    return self.extension == extension
  
  @classmethod
  def required_extensions(cls) -> List[Ext]:
    """
    Returns a list of required file extensions.

    This method should be overridden by subclasses.
    """
    return []
  
  @classmethod
  def from_content(cls, content: str, path: str) -> 'File':
    """
    Creates a new file from the specified content.

    Arguments:
      - content: The content of the file
      - path: The path to save the file
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
      os.makedirs(directory)
    with open(path, "w") as f:
      f.write(content)
    return cls(path)