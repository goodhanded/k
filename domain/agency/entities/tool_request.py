from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ToolRequest:
    """
    A request to execute a particular method on a tool, with structured params.
    """
    method: str
    params: Dict[str, Any]