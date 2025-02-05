import os
import tempfile
import unittest

from infrastructure.traceback.prompt_builder import TracebackPromptBuilder

class DummyClipboard:
    def __init__(self, initial=""):
        self.value = initial
    def get(self):
        return self.value
    def set(self, content):
        self.value = content

class TestTracebackPromptBuilder(unittest.TestCase):
    def test_extract_filepaths_for_python_traceback(self):
        # Create a temporary python file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as tmp:
            tmp.write("print('Hello world')")
            tmp_filepath = tmp.name
        
        # Construct a fake Python traceback string including the temporary file
        traceback_str = f'  File "{tmp_filepath}", line 10, in test_function\nError occurred'
        clipboard = DummyClipboard(traceback_str)
        builder = TracebackPromptBuilder(clipboard)
        filepaths = builder._extract_filepaths(traceback_str)
        self.assertIn(tmp_filepath, filepaths, "Failed to extract file path from Python traceback")
        os.remove(tmp_filepath)

    def test_build_prompt_includes_code_fences_and_traceback(self):
        # Create a temporary python file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".py") as tmp:
            tmp.write("print('Dummy code')")
            tmp_filepath = tmp.name
        
        # Fake traceback string containing the temp file path
        traceback_str = f'  File "{tmp_filepath}", line 5, in dummy_func\nSome error occurred'
        clipboard = DummyClipboard(traceback_str)
        builder = TracebackPromptBuilder(clipboard)
        prompt = builder._build_prompt([tmp_filepath], traceback_str)
        self.assertIn(f"# {tmp_filepath}", prompt, "File header not included in prompt")
        self.assertIn("```python", prompt, "Code block fence for python not found")
        self.assertIn("```bash", prompt, "Traceback code block fence not found")
        os.remove(tmp_filepath)

if __name__ == "__main__":
    unittest.main()
