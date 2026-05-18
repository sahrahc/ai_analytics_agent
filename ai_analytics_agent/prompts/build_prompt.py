import json

from ai_analytics_agent.state import GraphState
from ai_analytics_agent.metadata.semantic_data import (
    models,
    relationships,
)  # noqa: F401
from ai_analytics_agent.prompts.prompt_template import (
    SYSTEM_PROMPTS,
    USER_PROMPTS,
    PROMPT_VERSION,
)

# -----------------------------------
# Build prompt
# -----------------------------------


def build_prompt(analysis_request: str, metadata_results: list):

    metadata_context = json.dumps(metadata_results, indent=2)

    system_prompt = SYSTEM_PROMPTS[PROMPT_VERSION]

    user_prompt = USER_PROMPTS[PROMPT_VERSION].format(
        analysis_request=analysis_request, metadata_context=metadata_context
    )

    print("Built prompt context with metric and semantic model")
    return system_prompt, user_prompt
