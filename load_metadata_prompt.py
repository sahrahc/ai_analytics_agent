import json
from state import GraphState

# input
ENTITIES_PATH = "output/semantic_context.json"
RELATIONSHIPS_PATH = "output/semantic_model_relationships.json"
METRICS_PATH = "output/semantic_model_metrics.json"

# output/working files
# combined semantic model: entities + relationships
SEMANTIC_MODEL_PATH = "output/semantic_model.json"


# -----------------------------------
# Node 1: Load models first
# note that it also saves it as a file for debugging
# needed to build prompt context
# -----------------------------------


def load_model(state: GraphState):

    with open(ENTITIES_PATH, "r") as f:
        entities = json.load(f)

    with open(RELATIONSHIPS_PATH, "r") as f:
        relationships = json.load(f)

    # combine entities and relationships into a single semantic model
    # save as file for use in documentation
    semantic_model = {"models": entities, "relationships": relationships}

    # save semantic model to file for debugging
    with open(SEMANTIC_MODEL_PATH, "w") as f:
        json.dump(semantic_model, f, indent=2)

    print(
        f"Saved {len(semantic_model)} semantic nodes (models and relationships) to {SEMANTIC_MODEL_PATH}"
    )

    return {"semantic_model": semantic_model}


# -----------------------------------
# Node 2: Load all metrics
# -----------------------------------


def load_metrics(state: GraphState):

    with open(METRICS_PATH, "r") as f:
        metrics = json.load(f)

    print(f"Loaded {len(metrics)} metrics from {METRICS_PATH}")
    return {"metrics": metrics}


# -----------------------------------
# Node 3: Build prompt context
# -----------------------------------


def build_prompt_context(state: GraphState):

    context = {
        "metric": state["target_metric"],
        "semantic_model": state["semantic_model"],
    }

    print("Built prompt context with metric and semantic model")
    return {"prompt_context": context}
