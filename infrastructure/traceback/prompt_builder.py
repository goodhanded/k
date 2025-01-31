#!/usr/bin/env python3
import re
import sys
import os
import pyperclip

class TracebackPromptBuilder:
    def __init__(self):
        # Regex to capture file path, line number, and function name
        # Example line: File "/path/to/file.py", line 32, in on_message
        self.traceback_file_regex = re.compile(
            r'File\s+"(?P<filepath>[^"]+)",\s+line\s+(?P<lineno>\d+),\s+in\s+(?P<func>\S+)'
        )

    def build(self) -> str:
        """
        Given a traceback string, extracts file paths (excluding those in 'venv'),
        reads and appends their source contents inside python code blocks,
        then appends the original traceback.
        Returns a single string that can be used as an LLM prompt.
        """

        traceback_str = pyperclip.paste().strip()
        if not traceback_str:
            print("No traceback found in clipboard.")
            sys.exit(1)

        filepaths = self._extract_filepaths(traceback_str)
        # We use an Ordered set logic or just keep track of unique paths in order
        unique_filepaths = []
        seen = set()

        for fp in filepaths:
            if fp not in seen:
                unique_filepaths.append(fp)
                seen.add(fp)

        # Build the output
        output_parts = []

        for filepath in unique_filepaths:
            code_content = self._read_file_safely(filepath)
            # You can optionally annotate the file and line number
            output_parts.append(f"# {filepath}\n```python\n{code_content}\n```")

        # Finally, append the original traceback
        output_parts.append("\n# Traceback\n```python\n" + traceback_str.strip() + "\n```")

        prompt = "\n\n".join(output_parts)
        pyperclip.copy(prompt)

    def _extract_filepaths(self, traceback_str: str):
        """
        Extract file paths from the traceback lines using a regex,
        excluding anything in 'venv'.
        """
        filepaths = []
        for match in self.traceback_file_regex.finditer(traceback_str):
            fp = match.group("filepath")
            if "venv" not in fp:  # Exclude venv files
                filepaths.append(fp)
        return filepaths

    def _read_file_safely(self, filepath: str) -> str:
        """
        Returns the file content if it can be read; otherwise
        returns a warning string that the file could not be opened.
        """
        if not os.path.exists(filepath):
            return f"# Could not find file: {filepath}"

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"# Error reading file {filepath}: {e}"
