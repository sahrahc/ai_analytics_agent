import json

from state import GraphState
from metadata.semantic_data import models, relationships  # noqa: F401

# -----------------------------------
# Build prompt
# -----------------------------------


def build_prompt(analysis_request: str, metadata_results: list):

    metadata_context = json.dumps(metadata_results, indent=2)

    system_prompt = """
    You are a expert analytics engineer.

    Your job:
    - Generate valid Snowflake SQL
    - Think step-by-step before generating SQL
    - Use ONLY the provided metadata
    - Respect metric definitions
    - Respect table grain
    - Do not invent joins or columns
    - Return structured JSON
    """

    user_prompt = f"""
    User request: {analysis_request}

    Relevant metadata:
        {metadata_context}

    Generate SQL:
    """

    print("Built prompt context with metric and semantic model")
    return system_prompt, user_prompt
