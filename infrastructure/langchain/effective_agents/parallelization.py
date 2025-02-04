from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END

llm = ChatOpenAI(model="o1-mini")

# Graph state
class State(TypedDict):
  topic: str
  joke: str
  story: str
  poem: str
  combined_output: str

# Nodes
def call_llm_1(state: State):
  """First LLM call to generate initial joke"""
  msg = llm.invoke(f"Write a joke about {state['topic']}")
  return {"joke": msg.content}

def call_llm_2(state: State):
  """Second LLM call to generate story"""
  msg = llm.invoke(f"Write a story about {state['topic']}")
  return {"story": msg.content}

def call_llm_3(state: State):
  """Third LLM call to generate poem"""
  msg = llm.invoke(f"Write a poem about {state['topic']}")
  return {"poem": msg.content}

def aggregator(state: State):
  """Combine the story and joke into a single output"""
  combined = f"Here's a story, a joke, and a poem about {state['topic']}!\n\n"
  combined += f"STORY: {state['story']}\n\n"
  combined += f"JOKE: {state['joke']}\n\n"
  combined += f"POEM: {state['poem']}"
  combined += f"\n\n--- --- ---\n\n"
  combined += f"Find a creative way to combine these elements into a single output!"
  msg = llm.invoke(combined)
  return {"combined_output": msg.content}


# Build workflow
parallel_builder = StateGraph(State)

# Add nodes to the graph
parallel_builder.add_node("call_llm_1", call_llm_1)
parallel_builder.add_node("call_llm_2", call_llm_2)
parallel_builder.add_node("call_llm_3", call_llm_3)
parallel_builder.add_node("aggregator", aggregator)

# Add edges to connect the nodes
parallel_builder.add_edge(START, "call_llm_1")
parallel_builder.add_edge(START, "call_llm_2")
parallel_builder.add_edge(START, "call_llm_3")
parallel_builder.add_edge("call_llm_1", "aggregator")
parallel_builder.add_edge("call_llm_2", "aggregator")
parallel_builder.add_edge("call_llm_3", "aggregator")
parallel_builder.add_edge("aggregator", END)

# Compile
chain = parallel_builder.compile()

# Run workflow
state = chain.invoke({"topic": "cats"})

print("Story:")
print(state["story"])
print("\n--- --- ---\n")
print("Joke:")
print(state["joke"])
print("\n--- --- ---\n")
print("Poem:")
print(state["poem"])
print("\n--- --- ---\n")
print("Combined output:")
print(state["combined_output"])