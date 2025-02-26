from application.agency.protocols.workflow import WorkflowProtocol
from langgraph.graph.state import CompiledStateGraph

class Workflow(WorkflowProtocol):
    def __init__(self, graph: CompiledStateGraph) -> None:
        self.graph = graph       

    def run(self, state: dict) -> dict:
        return self.graph.invoke(state)