import json
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from openai import OpenAI

# custom libraries
from ai_analytics_agent.state import GraphState
from ai_analytics_agent.embeddings.vector_store import retrieve_relevant_metadata
from ai_analytics_agent.prompts.build_prompt import build_prompt

# -----------------------------------
# Generate SQL using LLM
# -----------------------------------
OUTPUT_PATH = "output/generated_sql.sql"
LOG_FILE = "output/openai_response.log"

TOP_K = 2


# Build compact context
def generate_sql_mock(state: GraphState, config: RunnableConfig):

    analysis_request = state["analysis_request"]

    # Step 1: similarity search
    metadata_results = retrieve_relevant_metadata(
        analysis_request=analysis_request, top_k=TOP_K
    )
    print("Retrieved relevant metadata: ", json.dumps(metadata_results, indent=2))
    # Step 2: build prompt
    system_prompt, user_prompt = build_prompt(
        analysis_request=analysis_request, metadata_results=metadata_results
    )
    print("System prompt: ", system_prompt)
    print("User prompt: ", user_prompt)

    sql_query = """
SELECT
  c.year AS year,
  c.week AS week,
  SUM(f.revenue_usd) AS revenue_usd_weekly,
  SUM(f.cost_usd) AS cost_usd_weekly,
  CASE
    WHEN SUM(f.cost_usd) = 0 THEN NULL
    ELSE SUM(f.revenue_usd) / NULLIF(SUM(f.cost_usd), 0)
  END AS roas_weekly
FROM STREAMING_ADS.streaming_ads_schema.fct_campaign_daily f
JOIN STREAMING_ADS.streaming_ads_schema.dim_calendar c
  ON f.date_key = c.date_key
GROUP BY
  c.year,
  c.week
ORDER BY
  c.year,
  c.week;
    """

    print("Mock generated SQL")
    return {"sql": sql_query}
