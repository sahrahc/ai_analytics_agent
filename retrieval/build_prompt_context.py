from state import GraphState
from retrieval.semantic_data import models, relationships  # noqa: F401

# -----------------------------------
# Node 3: Build prompt context
# -----------------------------------


def build_prompt_context(state: GraphState):

    context = {
        "metric": state["target_metric"],
        "semantic_model": {
            "models": models,
            "relationships": relationships,
        },
    }

    print("Built prompt context with metric and semantic model")
    return {"prompt_context": context}
