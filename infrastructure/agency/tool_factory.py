from application.agency.dtos import ToolDTO
from domain.util.yaml import load_yaml
from .tool import Tool

class ToolFactory:
    def create(self, tool_name: str) -> ToolDTO:
        tool_yaml_key = ["tools", tool_name]
        try:
            tool_dto = ToolDTO.from_yaml('tools.yaml', tool_yaml_key)
        except ValueError as e:
            return None

        return Tool.from_dto(tool_dto)

    def create_all(self, tool_names: list[str]) -> list[ToolDTO]:


        tools = []
        for tool_name in tool_names:
            tool = self.create(tool_name)
            tools.append(self.create(tool_name))

        return tools