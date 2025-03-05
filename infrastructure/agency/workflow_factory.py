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
        conditional_dict = {}

        # Determine edges from the workflow definition
        # If the definition is a list, use it directly; if it's a dict, extract the 'edges' key and ignore any 'nodes' key
        if not isinstance(definition, list):
            raise ValueError("Workflow definition should be a list of edges.")

        for edge in definition:
            if isinstance(edge, str):
                # Parse concise edge notation: "from_node -> to_node"
                parts = edge.split("->")
                if len(parts) != 2:
                    raise ValueError(f"Edge definition '{edge}' is not in the format 'from -> to'.")
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

            elif isinstance(edge, dict):
                # Expecting dictionary with at least "from" and "to" keys
                if "from" not in edge or "to" not in edge:
                    raise ValueError("Edge dictionary must contain 'from' and 'to' keys.")
                from_node = edge["from"].strip()
                to_node = edge["to"].strip()

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

                if "condition" in edge:
                    # Accumulate conditional edges by their source node
                    conditional_dict.setdefault(from_node, []).append({
                        "to": to_node,
                        "condition": edge["condition"]
                    })
                else:
                    state_graph.add_edge(START if from_node == "START" else from_node,
                                         END if to_node == "END" else to_node)
            else:
                raise ValueError("Each edge must be either a string or a dictionary.")

        # Process conditional edges: for each source node, add a conditional routing function that evaluates in order
        for from_node, cond_list in conditional_dict.items():
            def condition_func(state, cond_list=cond_list):
                for cond in cond_list:
                    if eval(cond["condition"], {}, {"state": state}):
                        return END if cond["to"] == "END" else cond["to"]
                return END
            state_graph.add_conditional_edges(START if from_node == "START" else from_node, condition_func)

        return Workflow(state_graph.compile())
