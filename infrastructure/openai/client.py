from openai import OpenAI
from application.agency.protocols.llm_client import LLMClientProtocol

class OpenAIClient(LLMClientProtocol):

  def __init__(self, api_key: str):
    self.client = OpenAI(
      api_key = api_key
    )

  def get_models(self):
    return self.client.models.list()

  def chat(self, model: str, prompt: str) -> str:
    chat = self.client.chat.completions.create(
      messages=[
        {
          "role": "user",
          "content": prompt,
        }
      ],
      model=model,
    )

    return chat.choices[0].message.content