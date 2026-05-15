from agent.generate_sql import generate_sql
from langgraph.graph import StateGraph, END

# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

from state import GraphState

# validators
from ai_analytics_agent.validation.validate_static_sql import validate_static_sql
from ai_analytics_agent.validation.validate_semantic_sql import validate_semantic_sql
from ai_analytics_agent.validation.validate_database import validate_with_database

from ai_analytics_agent.agent.generate_sql import generate_sql

# from ai_analytics_agent.agent.generate_sql_mock import generate_sql_mock

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

# for E2E testing with mock SQL
# generate_sql = generate_sql_mock
gernate_sql = generate_sql
workflow = StateGraph(GraphState)

# from external components
workflow.add_node("generate_sql", generate_sql)
workflow.add_node("validate_static_sql", validate_static_sql)
workflow.add_node("validate_semantic_sql", validate_semantic_sql)
workflow.add_node("validate_with_database", validate_with_database)

workflow.set_entry_point("generate_sql")

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
