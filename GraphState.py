from typing import TypedDict
from openai import OpenAI
from sqlglot import exp

# -----------------------------------
# Graph State
# -----------------------------------

class GraphState(TypedDict):
    metric_name: str
    semantic_model: dict
    metrics: list
    metric_definition: dict
    prompt_context: dict
    sql: str
    parsed_sql: exp.Type
    validation_status: str
