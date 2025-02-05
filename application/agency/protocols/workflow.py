from typing import Protocol
from ..dtos import WorkflowResultDTO

class WorkflowProtocol(Protocol):
  def invoke(self, prompt: str) -> WorkflowResultDTO:
    pass
