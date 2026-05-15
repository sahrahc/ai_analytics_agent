import json

# input
ENTITIES_PATH = "output/semantic_context.json"
RELATIONSHIPS_PATH = "output/semantic_model_relationships.json"
METRICS_PATH = "output/semantic_model_metrics.json"

# -----------------------------------
# Node 1: Load models (entities)
# -----------------------------------


def load_semantic_models():

    with open(ENTITIES_PATH, "r") as f:
        entities = json.load(f)

    print(f"Loaded {len(entities)} models from {ENTITIES_PATH}")

    return entities


# -----------------------------------
# Node 2: Load relationships
# -----------------------------------


def load_relationships():
    with open(RELATIONSHIPS_PATH, "r") as f:
        relationships = json.load(f)

    print(f"Loaded {len(relationships)} relationships from {RELATIONSHIPS_PATH}")
    return relationships


# -----------------------------------
# Node 3: Load all metrics
# -----------------------------------


def load_metrics():

    with open(METRICS_PATH, "r") as f:
        metrics = json.load(f)

    print(f"Loaded {len(metrics)} metrics from {METRICS_PATH}")
    return metrics
