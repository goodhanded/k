import unittest

from application.agency.dtos.tool_dto import ToolDTO
from infrastructure.agency.services.tool import Tool


class TestToolFactory(unittest.TestCase):
    def test_tool_from_dto(self):
        tool_dto = ToolDTO(name="TestTool", description="A tool for testing", methods=[])
        tool = Tool.from_dto(tool_dto)
        self.assertEqual(tool.name, "TestTool")
        self.assertEqual(tool.description, "A tool for testing")


if __name__ == '__main__':
    unittest.main()
