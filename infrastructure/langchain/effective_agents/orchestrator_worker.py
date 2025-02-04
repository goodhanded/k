from typing_extensions import Literal, TypedDict
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Annotated, List
import operator

llm = ChatOpenAI(model="gpt-4o")

class Section(BaseModel):
  name: str = Field(description="Name for this section of the report.")
  description: str = Field(description="Brief overview of the main topics and concepts to be covered in this section.")

class Sections(BaseModel):
  sections: List[Section] = Field(description="Sections of the report.")

# Augment the LLM with schema for structured output
planner = llm.with_structured_output(Sections)

# Graph state
class State(TypedDict):
  topic: str # Report topic
  sections: list[Section] # List of report sections
  completed_sections: Annotated[list, operator.add] # All workers write to this key in parallel
  final_report: str # Final report

# Worker state
class WorkerState(TypedDict):
  section: Section
  completed_sections: Annotated[list, operator.add]

# Nodes
def orchesrator(state: State):
  """Orchestrator that generates a plan for the report"""

  # Generate queries
  report_sections = planner.invoke(
    [
      HumanMessage(content=f"Generate a plan for the report topic: {state['topic']}"),
    ]
  )

  return {"sections": report_sections.sections}

def llm_call(state: WorkerState):
  """Worker writes a section of the report"""

  # Generate content for the section
  section = llm.invoke(
    [
      HumanMessage(
        content=f"Write a report for the section with name: {state['section'].name} and description: {state['section'].description}"
      ),
    ]
  )

  # Write the updated section to completed sections
  return {"completed_sections": [section.content]}

def synthesizer(state: State):
  """Synthesize full report from completed sections"""

  # List of completed sections
  completed_sections = state["completed_sections"]

  # Format completed section to str to use as context for finl sections
  completed_report_sections = "\n\n---\n\n".join(completed_sections)

  return {"final_report": completed_report_sections}

# Conditional edge function to create llm_call workers that each write a section of the report
def assign_workers(state: State):
  """Assign a worker to each section of the plan"""

  # Kick off section writing in paralhel via Send() API
  return [Send("llm_call", {"section":  s}) for s in state["sections"]]

# Build workflow
orchestrator_worker_builder = StateGraph(State)

# Add nodes to the graph
orchestrator_worker_builder.add_node("orchestrator", orchesrator)
orchestrator_worker_builder.add_node("llm_call", llm_call)
orchestrator_worker_builder.add_node("synthesizer", synthesizer)

# Add edges to connect the nodes
orchestrator_worker_builder.add_edge(START, "orchestrator")
orchestrator_worker_builder.add_conditional_edges(
  "orchestrator", assign_workers, ["llm_call"]
)

orchestrator_worker_builder.add_edge("llm_call", "synthesizer")
orchestrator_worker_builder.add_edge("synthesizer", END)

# Compile
orchestrator_worker = orchestrator_worker_builder.compile()

# Run workflow
state = orchestrator_worker.invoke({"topic": "AI in Healthcare"})
print(state["final_report"])