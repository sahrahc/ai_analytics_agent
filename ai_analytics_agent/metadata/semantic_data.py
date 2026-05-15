import json
from ai_analytics_agent.metadata.load_metadata import (
    load_semantic_models,
    load_relationships,
    load_metrics,
)

# PLACEHOLDER this is actually config for the purposes of processing user requests.
# should be made read only and ideally scheduled to update based on metadata change frequency.
# class SemanticData:
models = load_semantic_models()
relationships = load_relationships()
metrics = load_metrics()

# save semantic model to file for debugging - this is really part ONE
# but writing to semantic_model file here to avoid duplicate processing.
# TODO: Move this code when scheduling semantic metadata processing.
SEMANTIC_MODEL_PATH = "output/semantic_model.json"
semantic_model = {"models": models, "relationships": relationships}
with open(SEMANTIC_MODEL_PATH, "w") as f:
    json.dump(semantic_model, f, indent=2)


# semantic_data = SemanticData()
