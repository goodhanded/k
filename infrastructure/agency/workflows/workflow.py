from application.agency import WorkflowProtocol
from domain.registry import Registry
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class Workflow(WorkflowProtocol):
    def __init__(self, node_registry: Registry, state_registry: Registry, name: str, definition: dict) -> None:

        self.name = name
        self.definition = definition
        self.state = state_registry.get(name)
        self.graph = StateGraph(self.state)

        if "nodes" not in definition:
            raise ValueError("Workflow definition must contain a 'nodes' key.")

        for node_alias in definition["nodes"]:
            if not isinstance(node_alias, str):
                raise ValueError("Node must be a string.")
            if not node_registry.exists(node_alias):
                raise ValueError(f"Node {node_alias} is not registered.")
            node = node_registry.get(node_alias)
            self.graph.add_node(node_alias, node)

        if "edges" not in definition:
            raise ValueError("Workflow definition must contain an 'edges' key.")

        conditional_routes = []
        for edge in definition["edges"]:
            if not isinstance(edge, dict) or "from" not in edge or "to" not in edge:
                raise ValueError("Edge must be a dictionary with 'from' and 'to' keys.")

            if "condition" in edge:
                if edge["from"] not in conditional_routes:
                    conditional_routes.append(edge["from"])
                    self.graph.add_conditional_edges(edge["from"], self.route_conditionally(edge["from"]))
            else:
                self.graph.add_edge(START if edge["from"] == "START" else edge["from"],
                                    END if edge["to"] == "END" else edge["to"])

        self.graph.compile()

    def route_conditionally(self, from_node: str) -> callable:
        def condition(state: dict) -> str:
            for edge in self.definition["edges"]:
                if edge["from"] == from_node:
                    if eval(edge["condition"], None, {"state": state}): # this is not risky because the condition is defined in the workflow definition
                        return END if edge["to"] == END else edge["to"]
            return END
        return condition                

    def run(self, state: dict) -> dict:
        return self.graph.invoke(state)