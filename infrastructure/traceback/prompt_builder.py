#!/usr/bin/env python3
import re
import sys
import os

from application.filesystem.protocols.clipboard import ClipboardProtocol

class TracebackPromptBuilder:
    """
    A class that gathers file references from both Python and Node.js tracebacks,
    excluding 'venv' and 'node_modules', then builds an LLM prompt with the files'
    source code plus the original traceback.
    """

    def __init__(self, clipboard: ClipboardProtocol):

        self.clipboard = clipboard

        # Regex to capture Python tracebacks of the form:
        #   File "/path/to/file.py", line 32, in on_message
        self.python_tb_pattern = re.compile(
            r'File\s+"(?P<filepath>[^"]+)",\s+line\s+(?P<lineno>\d+),\s+in\s+(?P<func>\S+)'
        )

        # Regex to capture Node.js–style stack frames (absolute or relative), e.g.:
        #   at myFunc (/absolute/path/to/file.js:12:3)
        #   at /absolute/path/to/file.js:12:3
        #   src/some/relative/path.ts:7:1 - error ...
        # We allow any leading chars on a line (e.g. "│  ").
        self.node_tb_pattern = re.compile(
            r'(?:'
            r'at .*?\((?P<filepath1>[^\s)]+):(?P<lineno1>\d+)(?::(?P<colno1>\d+))?\)'
            r'|'
            r'^.*?(?P<filepath2>[^\s:]+):(?P<lineno2>\d+)(?::(?P<colno2>\d+))?'
            r')',
            re.MULTILINE
        )

    def build(self):
        """
        1) Reads the traceback from the clipboard
        2) Extracts file paths (Python & Node)
        3) Reads & appends source contents in code blocks
        4) Appends original traceback
        5) Copies the final result to the clipboard
        """
        traceback_str = self.clipboard.get()
        if not traceback_str:
            print("No traceback found in clipboard.")
            sys.exit(1)

        filepaths = self._extract_filepaths(traceback_str)
        prompt = self._build_prompt(filepaths, traceback_str)
        self.clipboard.set(prompt)
        print("\nPrompt has been built and copied to clipboard.\n")

    def _extract_filepaths(self, traceback_str: str):
        filepaths = []

        # --- Python matches ---
        for match in self.python_tb_pattern.finditer(traceback_str):
            fp = match.group("filepath")
            if not self._is_excluded(fp):
                filepaths.append(fp)

        # --- Node.js matches ---
        for match in self.node_tb_pattern.finditer(traceback_str):
            fp = match.group("filepath1") or match.group("filepath2")
            if fp and not self._is_excluded(fp):
                filepaths.append(fp)

        # Remove duplicates but keep order
        seen = set()
        unique_filepaths = []
        for fp in filepaths:
            if fp not in seen:
                unique_filepaths.append(fp)
                seen.add(fp)

        return unique_filepaths

    def _is_excluded(self, filepath: str) -> bool:
        lower = filepath.lower()
        return "venv" in lower or "node_modules" in lower

    def _build_prompt(self, filepaths, traceback_str) -> str:
        output_parts = []

        for fp in filepaths:
            print(f"Reading: {fp}")
            code_content = self._read_file_safely(fp)
            fence_lang = self._guess_language(fp)
            output_parts.append(f"# {fp}\n```{fence_lang}\n{code_content}\n```")

        output_parts.append("\n# Traceback\n```bash\n" + traceback_str.strip() + "\n```")
        return "\n\n".join(output_parts)

    def _read_file_safely(self, filepath: str) -> str:
        # If you'd like to interpret relative paths from current working dir:
        # full_path = os.path.abspath(filepath)
        # if not os.path.exists(full_path):
        #     return f"# Could not find file: {filepath}"
        # ...
        if not os.path.exists(filepath):
            return f"# Could not find file: {filepath}"
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"# Error reading file {filepath}: {e}"

    def _guess_language(self, filepath: str) -> str:
        _, ext = os.path.splitext(filepath.lower())
        if ext == ".py":
            return "python"
        elif ext == ".js":
            return "javascript"
        elif ext == ".ts":
            return "typescript"
        else:
            return ""  # or 'plaintext'


if __name__ == "__main__":
    builder = TracebackPromptBuilder()
    builder.build()