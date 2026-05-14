import json
from datetime import datetime
from urllib import response

from ai_api_client import client
from langgraph.graph import StateGraph
from GraphState import GraphState

# -----------------------------------
# Generate SQL using LLM
# -----------------------------------
OUTPUT_PATH = "generated_sql.sql"
LOG_FILE = "openai_response.log"

# Build compact context
def generate_sql(state: GraphState):
    
    context = {
            "metric": state["metric_definition"],
            "semantic_model": state["semantic_model"]
    }

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
    Generate SQL for metric:

    {state['metric_name']}

    Context:
    {json.dumps(state['prompt_context'], indent=2)}
    """

    # POST https://api.openai.com/v1/responses
    response = client.responses.create(
        model="gpt-5-mini",
        reasoning={
            # "effort": "medium"
            "effort": "low" # for development
        },
        text={
            "format": {
                "type": "json_schema",
                "name": "sql_generation_response",
                "schema": {
                    "type": "object",
                    "properties": {
                        "metric_name": {
                            "type": "string"
                        },
                        "reasoning": {
                            "type": "string"
                        },
                        "sql": {
                            "type": "string"
                        },
                        "tables_used": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "columns_used": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "warnings": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }   
                    },
                    "required": [
                        "metric_name",
                        "reasoning",
                        "sql",
                        "tables_used",
                        "columns_used",
                        "warnings"
                    ],
                    "additionalProperties": False
                }
            }
        },
        input=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )
    
    timestamp = datetime.now()
    
    log_entry = {
        "timestamp": timestamp,
        "response_id": response.id,
        "model": response.model,
        "response_text": response.output_text,
        "full_response": response.model_dump()
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry, indent=2, default=str))
        f.write("\n\n")

    print(f"Response logged to {LOG_FILE}")
    
    # SQL and reasoning stored in output file
    raw_json_string = response.output_text

    try:
        # 2. Parse the string into a Python dictionary
        parsed_data = json.loads(raw_json_string)

        # 3. Access individual schema fields safely
        metric = parsed_data.get("metric_name")
        reasoning = parsed_data.get("reasoning")
        sql_query = parsed_data.get("sql")
        tables = parsed_data.get("tables_used", [])
        columns = parsed_data.get("columns_used", [])
        warnings = parsed_data.get("warnings", [])

        with open(OUTPUT_PATH, "a") as f:
            f.write('"""')
            f.write(f"Metric: {metric}\n")
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

    print('response from chatbot API: ', sql_query)

    return {
        "sql": sql_query
    }
