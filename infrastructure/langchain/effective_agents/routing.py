from typing_extensions import Literal, TypedDict
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOpenAI(model="o1-mini")

class Route(BaseModel):
  step: Literal["poem", "story", "joke"] = Field(
    None, description="The next step in the routing process"
  )
  
# Augment the LLM with schema for structured output
router = llm.with_structured_output(Route)

# Graph state
class State(TypedDict):
  input: str
  decision: str
  output: str

def call_llm_1(state: State):
  """First LLM call to generate initial joke"""
  result = llm.invoke(state['input'])
  return {"output": result.content}

def call_llm_2(state: State):
  """Second LLM call to generate story"""
  result = llm.invoke(state['input'])
  return {"output": result.content}

def call_llm_3(state: State):
  """Third LLM call to generate poem"""
  result = llm.invoke(state['input'])
  return {"output": result.content}

def llm_call_router(state: State):
  """Route the input to the appropriate node"""

  # Run the augmented LLM with structured output to serve as routing logic
  decision = router.invoke(
    [
      SystemMessage(
        content="Route the input to story, joke, or poem based on the user's request."
      ),
      HumanMessage(content=state['input'])
    ]
  )

  return {"decision": decision.step}

# Conditional edge function to route to the appropriate node
def route_decision(state: State):
  # Return the node name you want to visit next
  if state["decision"] == "joke":
    return "call_llm_1"
  elif state["decision"] == "story":
    return "call_llm_2"
  elif state["decision"] == "poem":
    return "call_llm_3" 