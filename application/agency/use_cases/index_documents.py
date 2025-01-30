from ..protocols.indexer import IndexerProtocol

class IndexDocumentsUseCase:
    def __init__(self, indexer: IndexerProtocol):
        self.indexer = indexer

    def execute(self):
        print('Indexing documents...')
        result = self.indexer.index()
        if result.success:
            print('Indexing complete.')
        else:
            print(f'Indexing failed: {result.message}')