from typing import Protocol
from ..dtos import WorkflowResultDTO

class WorkflowProtocol(Protocol):
  def run(self, prompt: str) -> WorkflowResultDTO:
    pass
