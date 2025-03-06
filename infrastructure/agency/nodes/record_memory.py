import os

from application.agency.protocols.workflow_node import WorkflowNodeProtocol

class RecordMemory(WorkflowNodeProtocol):
    """
    Workflow node that records the prompt and response used in generating the output to a memory file.
    It writes to '.k/memory.txt'. If the followup flag is True, it appends to the file, otherwise it overwrites it.
    The response can be a changeset (from pull request workflows) or advice (from code advice workflows).
    """
    def __call__(self, state: dict) -> dict:
        if "project_path" not in state:
            raise ValueError("project_path is required in state")
        if "prompt" not in state:
            raise ValueError("Memory requires 'prompt' in state")
        
        response = state.get("changeset") or state.get("advice")
        if response is None:
            raise ValueError("Memory requires either 'changeset' or 'advice' in state")
        
        project_path = state["project_path"]
        memory_file = os.path.join(project_path, ".k", "memory.txt")
        
        followup = state.get("followup", False)
        
        entry = f"Prompt:\n{state['prompt']}\n\nResponse:\n{response}\n\n---\n"
        mode = "a" if followup else "w"
        
        with open(memory_file, mode, encoding="utf-8") as f:
            f.write(entry)
        
        return {"progress": "Memory recorded."}
