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
def generate_sql(state: GraphState, config: RunnableConfig):

    system_prompt = """
    You are a senior analytics engineer.

    Generate valid Snowflake SQL using the provided semantic metadata.

    Instructions:
    - Think step-by-step before generating SQL
    - Respect metric definitions
    - Respect table grain
    - Do not invent joins or columns
    - Return structured JSON
    """

    user_prompt = f"""
    Generate SQL for the following analysis request, by identifying the correct set of metrics
    using the provided semantic context:

    {state['analysis_request']}

    Context:
    {json.dumps(state['prompt_context'], indent=2)}
    """

    openai_client = config.get("configurable", {}).get("openai_client")
    if not openai_client:
        raise RuntimeError("OpenAI client not found in config")

    # POST https://api.openai.com/v1/responses
    response = openai_client.responses.create(
        model="gpt-5-mini",
        reasoning={
            # "effort": "medium"
            "effort": "low"  # for development
        },
        text={
            "format": {
                "type": "json_schema",
                "name": "sql_generation_response",
                "schema": {
                    "type": "object",
                    "properties": {
                        "analysis_request": {"type": "string"},
                        "reasoning": {"type": "string"},
                        "sql": {"type": "string"},
                        "tables_used": {"type": "array", "items": {"type": "string"}},
                        "columns_used": {"type": "array", "items": {"type": "string"}},
                        "warnings": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": [
                        "analysis_request",
                        "reasoning",
                        "sql",
                        "tables_used",
                        "columns_used",
                        "warnings",
                    ],
                    "additionalProperties": False,
                },
            }
        },
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    timestamp = datetime.now()

    # TODO create class and reuse for consistent logging
    log_entry = {
        "timestamp": timestamp,
        "response_id": response.id,
        "model": response.model,
        "response_text": response.output_text,
        "full_response": response.model_dump(),
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry, indent=2, default=str))
        f.write("\n\n")

    print(f"LLM Response logged to {LOG_FILE}")

    # SQL and reasoning stored in output file
    raw_json_string = response.output_text

    try:
        # 2. Parse the string into a Python dictionary
        parsed_data = json.loads(raw_json_string)

        # 3. Access individual schema fields safely
        analysis_request = parsed_data.get("analysis_request")
        reasoning = parsed_data.get("reasoning")
        sql_query = parsed_data.get("sql")
        tables = parsed_data.get("tables_used", [])
        columns = parsed_data.get("columns_used", [])
        warnings = parsed_data.get("warnings", [])

        with open(OUTPUT_PATH, "a") as f:
            f.write('"""')
            f.write(f"Analysis Request: {analysis_request}\n")
            f.write(f"Reasoning: {reasoning}\n")
            f.write(f"Tables Used: {tables}\n")
            f.write(f"Columns Used: {columns}\n")
            f.write(f"Warnings: {warnings}\n")
            f.write('"""')
            f.write("\n\n")
            f.write(sql_query)

        print(f"Saved output to {OUTPUT_PATH}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse response as JSON: {e}")

    print("response from chatbot API: ", sql_query)

    return {"sql": sql_query}
