import os
from application.agency import WorkflowProtocol
from langgraph.graph.state import CompiledStateGraph

class Workflow(WorkflowProtocol):
    def __init__(self, graph: CompiledStateGraph) -> None:
        self.graph = graph
        self.thread_id = self._get_last_thread_id()
        self.config = {"configurable": {"thread_id": self.thread_id}}


    def run(self, state: dict) -> dict:
        return self.graph.invoke(state, config=self.config)
    
    def _get_last_thread_id(self) -> int:
        # Read the last thread id from .k/last_thread.txt
        try:
            with open(os.path.join(".k", "last_thread.txt"), "r", encoding="utf-8") as f:
                return int(f.read())
        except FileNotFoundError:
            # write the last thread id to .k/last_thread.txt
            with open(os.path.join(".k", "last_thread.txt"), "w", encoding="utf-8") as f:
                f.write("1")
            return 1