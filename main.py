import sys
import snowflake.connector
from openai import OpenAI
from langchain_core.runnables import RunnableConfig

from graph import lang_graph
from state import GraphState
from config import settings

# -----------------------------------
# Config
# Single session, this code is not
# configured for multi-threading or
#   multiple concurrent executions.
# -----------------------------------

# -----------------------------------
# Store request on initial state
# -----------------------------------

analysis_request = sys.argv[1] if len(sys.argv) > 1 else None

if analysis_request is None:
    print("Error: No parameter provided.")
    sys.exit(1)
else:
    print(f"Runtime parameter received: {analysis_request}")

# -----------------------------------
# Runtime configuration for LangGraph
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

try:
    # 2. Bundle the thread_id (for LangGraph) and sf_session (for your code)
    lang_graph_config: RunnableConfig = {
        "configurable": {
            "thread_id": "sequential_session_101",  # Required by checkpointer
            "db_connection": db_connection,  # Passed directly to nodes
            "openai_client": client,  # Passed directly to nodes
        }
    }

    # -----------------------------------
    # Execute
    # -----------------------------------

    initial_state: GraphState = {
        "analysis_request": analysis_request,
        "target_metric": {},
        "semantic_model": {"models": [], "relationships": []},
        "metrics": [],
        "prompt_context": {},
        "sql": "",
        "parsed_sql": None,
        "validation_status": "",
    }

    result = lang_graph.invoke(initial_state, config=lang_graph_config)

finally:
    db_connection.close()
