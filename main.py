import json
import sys
import uuid

from openai import OpenAI, models
from langgraph.graph import StateGraph, END
#from langgraph.checkpoint.memory import MemorySaver
#from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

from GraphState import GraphState
from validate_static_sql import validate_static_sql
from validate_semantic_sql import validate_semantic_sql
from generate_sql import generate_sql

# -----------------------------------
# Config
# -----------------------------------

# input
ENTITIES_PATH = "output/semantic_context.json"
RELATIONSHIPS_PATH = "output/semantic_model_relationships.json"
METRICS_PATH = "output/semantic_model_metrics.json"

# output/working files
# combined semantic model: entities + relationships
SEMANTIC_MODEL_PATH = "output/semantic_model.json"

# TODO: user to provide English description of the analysis they want
input_metric = sys.argv[1] if len(sys.argv) > 1 else None

if input_metric is None:
    print("Error: No parameter provided.")
    sys.exit(1)
else:
    print(f"Runtime parameter received: {input_metric}")

client = OpenAI()

# -----------------------------------
# Node 0: Set input metric
# -----------------------------------
def set_input_metric(state: GraphState):
    return {
        "metric_name": input_metric
    }

# -----------------------------------
# Node 1: Load metadata
# -----------------------------------

def load_metadata(state: GraphState):

    with open(ENTITIES_PATH, "r") as f:
        entities = json.load(f)

    with open(RELATIONSHIPS_PATH, "r") as f:
        relationships = json.load(f)

    with open(METRICS_PATH, "r") as f:
        metrics = json.load(f)

    # combine entities and relationships into a single semantic model
    # save as file for use in documentation
    semantic_model = {
        "models": entities,
        "relationships": relationships,
    },

    with open(SEMANTIC_MODEL_PATH, "w") as f:
        json.dump(semantic_model[0], f, indent=2)

    print(f"Saved {len(semantic_model)} semantic models to {SEMANTIC_MODEL_PATH}")

    return {
        "semantic_model": semantic_model,
        "metrics": metrics
    }

# -----------------------------------
# Node 2: Retrieve metric definition
# -----------------------------------

def retrieve_metric(state: GraphState):

    metric_name = state["metric_name"]

    metric = next(
        m for m in state["metrics"]
        if m["metric_name"] == metric_name
    )

    return {
        "metric_definition": metric
    }

# -----------------------------------
# Node 3: Build prompt context
# -----------------------------------

def build_prompt_context(state: GraphState):

    context = {
        "metric": state["metric_definition"],
        "semantic_model": state["semantic_model"]
    }

    return {
        "prompt_context": context
    }

# -----------------------------------
# Build LangGraph
# -----------------------------------

#safe_serializer = JsonPlusSerializer(
#    all=["messages"]
#) 

# Pass the configured serializer directly into your checkpointer
#memory = MemorySaver(serde=safe_serializer)
#new_thread_id = str(uuid.uuid4()) 
#config = {"configurable": {"thread_id": new_thread_id}}

generate_sql= generate_sql

workflow = StateGraph(GraphState)

workflow.add_node("set_input_metric", set_input_metric)
workflow.add_node("load_metadata", load_metadata)
workflow.add_node("retrieve_metric", retrieve_metric)
workflow.add_node("build_prompt_context", build_prompt_context)
# from external components
workflow.add_node("generate_sql", generate_sql)
workflow.add_node("validate_static_sql", validate_static_sql)
workflow.add_node("validate_semantic_sql", validate_semantic_sql)

workflow.set_entry_point("set_input_metric")

workflow.add_edge("set_input_metric", "load_metadata")
workflow.add_edge("load_metadata", "retrieve_metric")
workflow.add_edge("retrieve_metric", "build_prompt_context")
workflow.add_edge("build_prompt_context", "generate_sql")
workflow.add_edge("generate_sql", "validate_static_sql")
workflow.add_edge("validate_static_sql", "validate_semantic_sql")
workflow.add_edge("validate_semantic_sql", END)

# TODO: circle back to sql generation step if any of the validation steps failed
# but only retry once.
# workflow.add_edge("validate_static_sql", END)
# TODO: add human intervention step

#graph = workflow.compile(checkpointer=memory)
graph = workflow.compile()

# -----------------------------------
# Execute
# -----------------------------------

result = graph.invoke({"message": "Hello, World!"}) # type: ignore

