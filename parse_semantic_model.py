import json
from pathlib import Path

import yaml

###############################################################
# Parse relationships and metrics from semantic fact yaml files
# one component for both because simple metrics generated
# out of a single table are defined with the table.
#
# derived metrics from multiple tables are defined in a separate
# component.
###############################################################

# inputs
YAML_PATH = "input/facts.yaml"

# outputs
METRICS_OUTPUT_PATH = "output/semantic_model_metrics.json"
REL_OUTPUT_PATH = "output/semantic_model_relationships.json"

###############################################################

with open(YAML_PATH, "r") as f:
    data = yaml.safe_load(f)

relationships = []
metrics = []

for model in data.get("models", []):
    model_name = model["name"]

    # reltionships
    for column in model.get("columns", []):
        entity = column.get("entity")

        if not entity:
            continue

        if entity.get("type") != "foreign":
            continue

        relationships.append({
            "from_model": model_name,
            "from_column": column["name"],
            "to_model": entity["name"],
            # start schema only has M:1 relationships from fact to dimension tables
            "relationship_type": "many_to_one"
        })

    # single table metrics
    for metric in model.get("metrics", []):
        metrics.append({
            "model": model_name,
            "metric_name": metric["name"],
            "metric_type": metric.get("type", "simple"),
            "aggregation": metric.get("agg"),
            "expression": metric.get("expr"),
            "numerator": metric.get("numerator"),
            "denominator": metric.get("denominator"),
            "label": metric.get("label"),
            "description": metric.get("description")
        })

# =========================================================
# WRITE OUTPUT
# =========================================================

with open(METRICS_OUTPUT_PATH, "w") as f:
    json.dump(metrics, f, indent=2)

print(f"Saved {len(metrics)} metrics to {METRICS_OUTPUT_PATH}")


with open(REL_OUTPUT_PATH, "w") as f:
    json.dump(relationships, f, indent=2)

print(f"Saved {len(relationships)} relationships to {REL_OUTPUT_PATH}")
