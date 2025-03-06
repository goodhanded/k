import os
from typing import Optional


def find_project_root() -> Optional[str]:
    """
    Traverses upward from the current directory to find a directory containing the '.k' folder.
    Returns the project root path if found, otherwise None.
    """
    current_dir = os.getcwd()
    while True:
        if os.path.isdir(os.path.join(current_dir, ".k")):
            return current_dir
        parent = os.path.dirname(current_dir)
        if parent == current_dir:
            return None
        current_dir = parent
