from application.agency import ToolProtocol, ToolDTO

class Tool(ToolProtocol):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.__str__()

    @staticmethod
    def from_dto(tool_dto: ToolDTO):
        tool = Tool(tool_dto.name, tool_dto.description)
        return tool