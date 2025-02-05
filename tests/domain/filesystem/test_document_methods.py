import os
import tempfile
import unittest

from domain.filesystem.entities.document import Document


class TestDocumentMethods(unittest.TestCase):
    def test_document_round_trip(self):
        original_content = "Sample document content."
        with tempfile.TemporaryDirectory() as tmpdirname:
            file_path = os.path.join(tmpdirname, "test.md")
            doc = Document(original_content)
            # Save the document to file
            doc.to_file(file_path)
            # Now read document from file
            loaded_doc = Document.from_path(file_path)
            self.assertIsNotNone(loaded_doc)
            self.assertEqual(loaded_doc.content, original_content)


if __name__ == '__main__':
    unittest.main()
