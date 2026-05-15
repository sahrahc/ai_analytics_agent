import json

# --------------------------------------------------
# Embedding Helper functions
# --------------------------------------------------


def build_embedding_text(entity_type: str, payload: dict) -> str:
    """
    Convert metadata dictionary into embedding text.
    """

    print("\n\npayload in build_embedding_text:", payload)

    if entity_type == "model":
        # just get the name
        columns = ", ".join(
            col["name"] if isinstance(col, dict) else str(col)
            for col in payload.get("columns", [])
        )
        return (
            f"Model: {payload['name']}. "
            f"Description: {payload.get('description', '')}. "
            f"Columns: {columns}"
        )

    if entity_type == "relationship":
        return (
            f"Relationship from {payload['from_model']} "
            f"to {payload['to_model']}. "
            f"Type: {payload['relationship_type']}. "
            f"Join key: {payload['from_column']}"
        )

    if entity_type == "metric":
        return (
            f"Metric: {payload['metric_name']}. "
            f"Description: {payload.get('description', '')}. "
            f"Primary Model: {payload.get('model', '')}. "
            f"Aggregation: {payload.get('aggregation', '')}"
            f"Primary Column: {payload.get('expression', '')}"
            f"Numerator: {payload.get('numerator', '')}"
            f"Denominator: {payload.get('denominator', '')}"
        )

    return json.dumps(payload)


def vector_to_pg(vector):
    """
    Convert Python list to pgvector string format.
    """
    return "[" + ",".join(str(x) for x in vector) + "]"
