from dataclasses import dataclass
from typing import Dict, Any
from application.dto import DataTransferObject

@dataclass
class ToolRequestDTO(DataTransferObject):
    """
    A request to execute a particular method on a tool, with structured params.
    """
    method: str
    params: Dict[str, Any]