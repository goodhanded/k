from application.intelligence import NoteVaultInterface
from ..indexer_interface import IndexerInterface

class IndexDocumentsUseCase:
    def __init__(self, indexer: IndexerInterface):
        self.indexer = indexer

    def execute(self):
        print('Indexing documents...')
        result = self.indexer.index()
        if result.success:
            print('Indexing complete.')
        else:
            print(f'Indexing failed: {result.message}')