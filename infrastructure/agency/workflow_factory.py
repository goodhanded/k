from application.agency.protocols.workflow import WorkflowProtocol
from domain.registry.entities.registry import Registry
from langgraph.graph import StateGraph, START, END

from .workflow import Workflow


class WorkflowFactory(WorkflowProtocol):
    def __init__(self, node_registry: Registry, state_registry: Registry, workflows: dict) -> None:
        self.node_registry = node_registry
        self.state_registry = state_registry
        self.workflows = workflows

    def create(self, workflow_name: str) -> WorkflowProtocol:
        definition = self.workflows[workflow_name]
        state = self.state_registry.get(workflow_name)
        state_graph = StateGraph(state)
        nodes_added = set()

        # New concise format: if definition is a list of edge strings
        if isinstance(definition, list):
            for edge_str in definition:
                parts = edge_str.split("->")
                if len(parts) != 2:
                    raise ValueError(f"Edge definition '{edge_str}' is not in the format 'from -> to'.")
                from_node = parts[0].strip()
                to_node = parts[1].strip()

                if from_node != "START" and from_node not in nodes_added:
                    if not self.node_registry.exists(from_node):
                        raise ValueError(f"Node {from_node} is not registered.")
                    state_graph.add_node(from_node, self.node_registry.get(from_node))
                    nodes_added.add(from_node)
                if to_node != "END" and to_node not in nodes_added:
                    if not self.node_registry.exists(to_node):
                        raise ValueError(f"Node {to_node} is not registered.")
                    state_graph.add_node(to_node, self.node_registry.get(to_node))
                    nodes_added.add(to_node)

                state_graph.add_edge(START if from_node == "START" else from_node,
                                      END if to_node == "END" else to_node)
        else:
            # Fallback legacy behavior
            if "nodes" not in definition:
                raise ValueError("Workflow definition must contain a 'nodes' key.")

            for node_alias in definition["nodes"]:
                if not isinstance(node_alias, str):
                    raise ValueError("Node must be a string.")
                if not self.node_registry.exists(node_alias):
                    raise ValueError(f"Node {node_alias} is not registered.")
                state_graph.add_node(node_alias, self.node_registry.get(node_alias))

            if "edges" not in definition:
                raise ValueError("Workflow definition must contain an 'edges' key.")

            conditional_routes = []
            for edge in definition["edges"]:
                if not isinstance(edge, dict) or "from" not in edge or "to" not in edge:
                    raise ValueError("Edge must be a dictionary with 'from' and 'to' keys.")

                if "condition" in edge:
                    if edge["from"] not in conditional_routes:
                        conditional_routes.append(edge["from"])
                        state_graph.add_conditional_edges(edge["from"], self.route_conditionally(edge["from"]))
                else:
                    state_graph.add_edge(START if edge["from"] == "START" else edge["from"],
                                          END if edge["to"] == "END" else edge["to"])

        return Workflow(state_graph.compile())

    def route_conditionally(self, from_node: str) -> callable:
        def condition(state: dict) -> str:
            for edge in self.definition["edges"]:
                if edge["from"] == from_node:
                    if eval(edge["condition"], None, {"state": state}):  # this is not risky because the condition is defined in the workflow definition
                        return END if edge["to"] == END else edge["to"]
            return END
        return condition
