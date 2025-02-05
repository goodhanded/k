import unittest
from application.agency.use_cases.index_documents import IndexDocumentsUseCase
from domain.search.entities.index_result import IndexResult


class DummyIndexer:
    def index(self) -> IndexResult:
        return IndexResult(success=True, message="Indexing complete")


class TestIndexDocumentsUseCase(unittest.TestCase):
    def test_execute(self) -> None:
        indexer = DummyIndexer()
        use_case = IndexDocumentsUseCase(indexer)
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        use_case.execute()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Indexing complete", output)


if __name__ == '__main__':
    unittest.main()
