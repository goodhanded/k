from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END

llm = ChatOpenAI(model="o3-mini")

# class SearchQuery(BaseModel):
#   search_query: str = Field(None, description="Query that is optimized web search.")
#   justification: str = Field(None, justification="Why this query is relevant to the user's request.")

# structured_llm = llm.with_structured_output(SearchQuery)

# Graph state
class State(TypedDict):
  topic: str
  joke: str
  improved_joke: str
  final_joke: str

# Nodes
def generate_joke(state: State):
  """First LLM call to generate initial joke"""
  msg = llm.invoke(f"Write a short joke about {state['topic']}")
  return {"joke": msg.content}

def improve_joke(state: State):
  """Second LLM call to improve joke"""
  msg = llm.invoke(f"Make this joke funnier by adding wordplay: {state['joke']}")
  return {"improved_joke": msg.content}

def polish_joke(state: State):
  """Third LLM call to polish joke"""
  msg = llm.invoke(f"Add a surprising twist to this joke: {state['improved_joke']}")
  return {"final_joke": msg.content}

def check_punchline(state: State):
  """Check if the joke has a punchline"""
  if "?" in state["joke"] or "!" in state["joke"]:
    return "Pass"
  return "Fail"

# Build workflow
workflow = StateGraph(State)

# Add nodes to the graph
workflow.add_node("generate_joke", generate_joke)
workflow.add_node("improve_joke", improve_joke)
workflow.add_node("polish_joke", polish_joke)

# Add edges to connect the nodes
workflow.add_edge(START, "generate_joke")
workflow.add_conditional_edges("generate_joke", check_punchline, {"Pass": "improve_joke", "Fail": END})
workflow.add_edge("improve_joke", "polish_joke")
workflow.add_edge("polish_joke", END)

# Compile
chain = workflow.compile()

# Run workflow
state = chain.invoke({"topic": "cats"})

print("Initial joke:")
print(state["joke"])
print("\n--- --- ---\n")
if "improved_joke" in state:
  print("Improved joke:")
  print(state["improved_joke"])
  print("\n--- --- ---\n")

  print("Final joke:")
  print(state["final_joke"])
else:
  print("Joke failed qulity gate - no punchline detected!")

