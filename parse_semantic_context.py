import json
from pathlib import Path

MANIFEST_PATH = "input/manifest.json"
CATALOG_PATH = "input/catalog.json"

###############################################################

# get the table name and ID and column names from manifest, as it is the most comprehensive source of tables
manifest = json.loads(Path(MANIFEST_PATH).read_text())
# get the 
catalog = json.loads(Path(CATALOG_PATH).read_text())

models = {}
relationships = []

# Parse dbt models
for unique_id, node in manifest["nodes"].items():
    if node["resource_type"] != "model":
        continue

    model_name = node["name"]
    # only include facts and dimensions, exclude marts and staging tables
    if model_name[0:3] not in ('fct','dim'):
        continue

    print('Parsing model:', model_name)
    catalog_col = (
        catalog.get("nodes", {})
        .get(unique_id, {})
        .get("columns", {})
            #.get(col_name.upper(), {})
    )
    columns = []

    # catalog has the comprehensive list of columns
    for col_name, col_meta in catalog_col.items():
        col_name = col_name.lower()

        # however only manifest has descriptions
        manifest_col_meta = node.get("columns", {}).get(col_name, {})

        columns.append({
            "name": col_name,
            "description": manifest_col_meta.get("description"),
            "data_type": col_meta.get("type").lower() if col_meta.get("type") else None,
        })

    models[model_name] = {
        "name": model_name,
        "description": node.get("description"),
        "database": node.get("database"),
        "schema": node.get("schema"),
        "alias": node.get("alias"),
        "columns": columns,
        "depends_on": node.get("depends_on", {}).get("nodes", []),
    }

# single json file containing all semantic context
# semantic_context = {
#    "models": list(models.values()),
#    "relationships": relationships,
# }

models = list(models.values())

# =========================================================
# WRITE OUTPUT
# =========================================================

OUTPUT_PATH = "output/semantic_context.json"

with open(OUTPUT_PATH, "w") as f:
    json.dump(models, f, indent=2)

print(f"Saved {len(models)} entities/models to {OUTPUT_PATH}")
