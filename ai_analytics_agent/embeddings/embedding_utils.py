import json

# --------------------------------------------------
# Embedding Helper functions
# --------------------------------------------------


def build_embedding_text(entity_type: str, payload: dict) -> str:
    """
    Convert metadata dictionary into embedding text.
    """

    if entity_type == "model":
        return (
            f"Model: {payload['model_name']}. "
            f"Description: {payload.get('description', '')}. "
            f"Columns: {', '.join(payload.get('columns', []))}"
        )

    if entity_type == "relationship":
        return (
            f"Relationship from {payload['source_model']} "
            f"to {payload['target_model']}. "
            f"Type: {payload['relationship_type']}. "
            f"Join key: {payload['join_key']}"
        )

    if entity_type == "metric":
        return (
            f"Metric: {payload['metric_name']}. "
            f"Description: {payload.get('description', '')}. "
            f"SQL: {payload.get('sql', '')}"
        )

    return json.dumps(payload)


def vector_to_pg(vector):
    """
    Convert Python list to pgvector string format.
    """
    return "[" + ",".join(str(x) for x in vector) + "]"
