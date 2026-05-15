from langgraph.graph import StateGraph, END

# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

from retrieval.identify_metrics import identify_metrics
from state import GraphState

# generators
from retrieval.build_prompt_context import build_prompt_context

# validators
from validator.validate_static_sql import validate_static_sql
from validator.validate_semantic_sql import validate_semantic_sql
from validator.validate_database import validate_with_database
from generator.generate_sql_mock import generate_sql_mock

# -----------------------------------
# Build LangGraph
# -----------------------------------

# safe_serializer = JsonPlusSerializer(
#    all=["messages"]
# )

# TODO: add checkpoint for human in the loop intervention if validation fails
# Pass the configured serializer directly into your checkpointer
# memory = MemorySaver(serde=safe_serializer)
# new_thread_id = str(uuid.uuid4())
# config = {"configurable": {"thread_id": new_thread_id}}

generate_sql = generate_sql_mock

workflow = StateGraph(GraphState)

workflow.add_node("build_prompt_context", build_prompt_context)
# from external components
workflow.add_node("generate_sql", generate_sql)
workflow.add_node("validate_static_sql", validate_static_sql)
workflow.add_node("validate_semantic_sql", validate_semantic_sql)
workflow.add_node("validate_with_database", validate_with_database)

workflow.set_entry_point("build_prompt_context")

workflow.add_edge("build_prompt_context", "generate_sql")
workflow.add_edge("generate_sql", "validate_static_sql")
workflow.add_edge("validate_static_sql", "validate_semantic_sql")
workflow.add_edge("validate_semantic_sql", "validate_with_database")
workflow.add_edge("validate_with_database", END)

# TODO: circle back to sql generation step if any of the validation steps failed
# but only retry once.
# workflow.add_edge("validate_static_sql", END)
# TODO: add human intervention step

# graph = workflow.compile(checkpointer=memory)
lang_graph = workflow.compile()
