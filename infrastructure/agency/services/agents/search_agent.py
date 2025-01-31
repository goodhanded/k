from datetime import datetime
from domain.filesystem import DocumentCollection
from application.agency import AgentProtocol, ToolProtocol
from application.search import SearchEngineProtocol
from application.intelligence import LLMClientProtocol
from application.agency.dtos import AgentResponseDTO
from infrastructure.langchain import LangchainDocumentMapper

class SearchAgent(AgentProtocol):
    def __init__(self, search_engine: SearchEngineProtocol, mapper: LangchainDocumentMapper, llm: LLMClientProtocol, model: str):
        self.search_engine = search_engine
        self.mapper = mapper
        self.llm = llm

        self.name = 'Search Agent'
        self.model = model
        self.description = 'This agent conducts a similarity search using FAISS.'

        
    def invoke(self, prompt: str):

        print('Searching...')
        search_result = self.search_engine.search(prompt)

        responseDTO = AgentResponseDTO(
            agent=self.name,
            timestamp=datetime.now(),
            prompt=prompt,
            success=True,
            response=search_result.docs
        )

        return responseDTO
    def add_tools(self, tools: list[ToolProtocol]):
        self.add_tool(tool for tool in tools)
    def add_tool(self, tool: ToolProtocol):
        self.tools.append(tool)
    def __str__(self):
        return f'{self.name} ({self.model}): {self.description}'