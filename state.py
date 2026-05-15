import json
from typing import TypedDict
from sqlglot import expressions

# -----------------------------------
# Graph State - stores the state
# of the LangGraph workflow during
# execution and is passed between nodes
# -----------------------------------


class GraphState(TypedDict):
    analysis_request: str
    # prompt_context: dict
    sql: str
    parsed_sql: expressions.Select | None
    validation_status: str
