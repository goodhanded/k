import yaml
from typing import Dict, Any, Optional
from abc import abstractmethod

from .tool_request import ToolRequest
from domain.util.yaml import load_yaml

class AgentTool:
    """
    A base tool that:
      1) Receives a contract describing methods, params, returns, etc.
      2) Validates a ToolRequest against that contract
      3) If valid, dispatches to a handler method on the subclass
    """

    def __init__(self, definition):
        """
        :param definition: dictionary definition loaded from tools.yaml
        """
        self._contract_methods = {
            m["name"]: m for m in definition.get("methods", [])
        }
        self._examples = definition.get("examples", [])
        self.name = definition["name"]
        self.description = definition["description"]
 
    def __str__(self):
        return f"{self.name} Tool"
    
    def __repr__(self):
        return f"{self.name} Tool"

    def execute(self, request: ToolRequest) -> str:
        """
        1) Validate the request against the contract
        2) If valid, dispatch to the appropriate handler method
        3) Return a JSON string or message
        """
        errors = self.validate_request(request)
        if errors:
            return f"Invalid request: {errors}"

        # Attempt to dispatch to a matching handler method.
        # By convention, we’ll call them _handle_{methodName}.
        method_handler_name = f"_handle_{request.method}"
        if not hasattr(self, method_handler_name):
            return f"No handler found for method '{request.method}'"
        
        handler = getattr(self, method_handler_name)
        result = handler(request.params)
        return result

    def validate_request(self, request: ToolRequest) -> Optional[str]:
        """
        Checks:
          1) Method in contract
          2) Required parameters present
          3) (Optional) Param type checks
        Return an error string if invalid, else None if all is good.
        """
        # Check if method is known
        if request.method not in self._contract_methods:
            return f"Unknown method: {request.method}"

        method_def = self._contract_methods[request.method]
        
        # Check required params
        required_errors = []
        for param_def in method_def.get("params", []):
            param_name = param_def["name"]
            if param_name not in request.params:
                required_errors.append(f"Missing required param '{param_name}'")
                continue

            # Check param types
            param_type = param_def["type"]
            if param_type == "string":
                if not isinstance(request.params[param_name], str):
                    required_errors.append(f"Param '{param_name}' must be a string")
            elif param_type == "integer":
                if not isinstance(request.params[param_name], int):
                    required_errors.append(f"Param '{param_name}' must be an integer")
            elif param_type == "array":
                if not isinstance(request.params[param_name], list):
                    required_errors.append(f"Param '{param_name}' must be an array")
            elif param_type == "object":
                if not isinstance(request.params[param_name], dict):
                    required_errors.append(f"Param '{param_name}' must be an object")
            elif param_type == "boolean":
                if not isinstance(request.params[param_name], bool):
                    required_errors.append(f"Param '{param_name}' must be a boolean")
            elif param_type == "number":
                if not isinstance(request.params[param_name], (int, float)):
                    required_errors.append(f"Param '{param_name}' must be a number")

        if required_errors:
            return "; ".join(required_errors)

        return None

    def build_usage_instructions(self) -> str:
        """
        Build a usage string describing the methods.
        """
        lines = [
            f"Tool Name: {self.name}",
            f"Description: {self.description}",
            "Methods:"
        ]
        for method_name, method_def in self._contract_methods.items():
            desc = method_def.get("description", "")
            lines.append(f"  - {method_name}: {desc}")

            param_lines = []
            for param in method_def.get("params", []):
                pname = param["name"]
                ptype = param["type"]
                pdesc = param.get("description", "")
                param_lines.append(f"    * {pname} ({ptype}): {pdesc}")
            if param_lines:
                lines.append("    Parameters:")
                lines.extend(param_lines)

        return "\n".join(lines)

    @abstractmethod
    def _handle_unknown(self, params: Dict[str, Any]) -> str:
        """
        Subclasses can override for a default handler or just omit usage.
        """
        return "Not implemented"