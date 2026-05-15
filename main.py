from asyncio import subprocess
import sys
from typing import cast

# third party libraries
import snowflake.connector
from openai import OpenAI
from langchain_core.runnables import RunnableConfig

# internal modules
from graph import lang_graph
from state import GraphState
from config import settings

from retrieval.identify_metrics import identify_metrics

# ----------------------------------------------------------------------
# There are two sections to this file, eventually to be two components:
#
# 1. Semantic metadata processing - scheduling dependent on metadata
# change frequency.
# 2. Analytics request processing - triggered by incoming request
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# PART ONE - Semantic metadata processing
# Comment out to be run as needed for now.
# ----------------------------------------------------------------------
# execute these separate files to refresh semantic metadata json files:
# - parser/parser_semantic_context.py -- loads entities/models
# - parser/parser_semantic_model_facts.py -- loads relationships and metrics
# output: three files in output/:
#   semantic_context.json,
#   semantic_model_relationships.json,
#   semantic_model_metrics.json

# ----------------------------------------------------------------------
# PART TWO - Analytics request processing
# ----------------------------------------------------------------------
# -----------------------------------
# 1. Store request on initial state
# -----------------------------------

analysis_request = sys.argv[1] if len(sys.argv) > 1 else None

if analysis_request is None:
    print("Error: No parameter provided.")
    sys.exit(1)
else:
    print(f"Runtime parameter received: {analysis_request}")


# 2. load semantic metadata for use by part 2.
from retrieval.semantic_data import metrics  # noqa: F401

# 3. retrieval
target_metric = identify_metrics(analysis_request, metrics)

# -----------------------------------
# Establish connection to Snowflake and OpenAI
# for Runtime configuration for LangGraph
# -----------------------------------

# Connect to Snowflake
db_connection = snowflake.connector.connect(
    user=settings.SNOWFLAKE_USER,
    account=settings.SNOWFLAKE_ACCOUNT,
    private_key=settings.private_key,
    authenticator="SNOWFLAKE_JWT",
    warehouse=settings.SNOWFLAKE_WAREHOUSE,
    database=settings.SNOWFLAKE_DATABASE,
    schema=settings.SNOWFLAKE_SCHEMA,
    role=settings.SNOWFLAKE_ROLE,
)

# own module to enable using same connection settings across multiple modules.
client = OpenAI()

# -----------------------------------
# Execute
# -----------------------------------

try:
    # 2. Bundle the thread_id (for LangGraph) and sf_session (for your code)
    lang_graph_config: RunnableConfig = {
        "configurable": {
            "thread_id": "sequential_session_101",  # Required by checkpointer
            "db_connection": db_connection,  # Passed directly to nodes
            "openai_client": client,  # Passed directly to nodes
        }
    }

    # explicit casting for type checking only
    initial_state: GraphState = {
        "analysis_request": "analysis_request",
        "target_metric": target_metric,
        "prompt_context": {},
        "sql": "",
        "parsed_sql": None,
        "validation_status": "",
    }

    result = lang_graph.invoke(initial_state, config=lang_graph_config)  # type: ignore

finally:
    db_connection.close()
