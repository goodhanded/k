from anthropic import Anthropic
from typing import List, Dict, Any
from application.agency.protocols.llm_client import LLMClientProtocol

class AnthropicClient(LLMClientProtocol):
    model: str = "claude-3-7-sonnet-latest"

    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

    def get_models(self) -> List[Dict[str, Any]]:
        """Get a list of available Anthropic models."""
        models = self.client.models.list()
        return [{"id": model.id, "name": model.display_name} 
                for model in models.data]

    def chat(self, model: str, prompt: str) -> str:
        """Send a chat message to the specified model."""
        message = self.client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text