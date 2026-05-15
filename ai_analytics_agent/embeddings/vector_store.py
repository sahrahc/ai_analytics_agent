from config import settings
from metadata_db import get_connection
from sentence_transformers import SentenceTransformer
from embeddings.embedding_utils import vector_to_pg
from rapidfuzz import fuzz

# --------------------------------------------------
# Utilities for retrieving relevant metadata based
# on semantic similarity search or fuzzy string matching.
# --------------------------------------------------


# --------------------------------------------------
# Option 1 - Semantic similarity search
# --------------------------------------------------

# Initialize embedding model
embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)


def retrieve_relevant_metadata(analysis_request: str, top_k: int = 5):
    """
    Perform a semantic similarity search against the schema_embeddings table.
    """
    query_embedding = embedding_model.encode(analysis_request).tolist()
    query_vector = vector_to_pg(query_embedding)

    with get_connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    entity_type,
                    entity_name,
                    metadata,
                    embedding <=> %s::vector AS distance
                FROM ads_schema_embeddings
                ORDER BY distance
                LIMIT %s
                """,
                (query_vector, top_k),
            )

            results = cursor.fetchall()

            parsed = []

            print("\nTop semantic matches:")
            for row in results:
                parsed.append(
                    {
                        "entity_type": row[0],
                        "entity_name": row[1],
                        "metadata": row[2],
                        "distance": float(row[3]),
                    }
                )

                # Printed after Top semantic matches
                print(row)

            return parsed


# -----------------------------------
# Option 2 - Simpler alternative using fuzzy string matching
# -----------------------------------


def identify_metrics(analysis_request: str, metrics: list):

    if metrics is None:
        raise Exception("Metrics not found in state.")

    scores = []

    for metric in metrics:

        score = fuzz.token_sort_ratio(analysis_request, metric["metric_name"])

        scores.append((score, metric))

    # only one value returned for development, can be expanded later
    return {"target_metric": max(scores, key=lambda x: x[0])[1]}
