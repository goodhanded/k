from typing import Protocol, List, Dict, Any

class LLMClientProtocol(Protocol):

    model: str

    def chat(self, model: str, prompt: str) -> str:
        pass
        
    def get_models(self) -> List[Dict[str, Any]]:
        pass