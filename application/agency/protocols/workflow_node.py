from typing import Protocol

class WorkflowNodeProtocol(Protocol):
  def __call__(self, state: dict) -> dict:
    pass