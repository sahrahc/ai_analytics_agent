import json
from datetime import datetime
from urllib import response

from state import GraphState
from langchain_core.runnables import RunnableConfig

from openai import OpenAI

# -----------------------------------
# Generate SQL using LLM
# -----------------------------------
OUTPUT_PATH = "output/generated_sql.sql"
LOG_FILE = "output/openai_response.log"


# Build compact context
def generate_sql_mock(state: GraphState, config: RunnableConfig):

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
