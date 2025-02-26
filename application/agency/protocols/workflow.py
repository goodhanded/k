from typing import Protocol
from ..dtos.workflow_result_dto import WorkflowResultDTO

class WorkflowProtocol(Protocol):
  def run(self, prompt: str) -> WorkflowResultDTO:
    pass
