from datetime import datetime
from application.agency import WorkflowProtocol
from application.search import SearchEngineProtocol
from application.intelligence import LLMClientProtocol
from application.agency.dtos import WorkflowResultDTO
from infrastructure.langchain import LangchainDocumentMapper

class SearchAgent(WorkflowProtocol):
    """
    Search Agent

    This agent conducts a similarity search using a search engine (like FAISS). It's not very useful at the moment.
    """
    def __init__(self, search_engine: SearchEngineProtocol, mapper: LangchainDocumentMapper, llm: LLMClientProtocol, model: str):
        self.search_engine = search_engine
        self.mapper = mapper
        self.llm = llm

        self.name = 'Search Agent'
        self.model = model
        self.description = 'This agent conducts a similarity search using a search engine (like FAISS).'

        
    def run(self, prompt: str):

        print('Searching...')
        search_result = self.search_engine.search(prompt)

        responseDTO = WorkflowResultDTO(
            workflow=self.name,
            timestamp=datetime.now(),
            prompt=prompt,
            success=True,
            response=search_result.docs
        )

        return responseDTO

    def __str__(self):
        return f'{self.name} ({self.model}): {self.description}'