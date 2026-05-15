import threading

import psycopg2

# metric definitions
# model descriptions
# column descriptions
# YAML docs
# join descriptions
# business glossary
# semantic aliases

# into embeddings (vectors).

# format:
# Metric: total_revenue
# Description: sum of completed order revenue

# Dimension: country
# Description: customer billing country

# Model: fct_orders
# Description: order-level commerce facts

"""
Requirements:
pip install psycopg2-binary pgvector sentence-transformers

Postgres setup:
CREATE EXTENSION IF NOT EXISTS vector;
"""

import json
import psycopg2
from psycopg2.extras import execute_values
from sentence_transformers import SentenceTransformer

# custom
from ai_analytics_agent import config
from ai_analytics_agent.metadata.semantic_data import (
    models,
    relationships,
    metrics,
)  # noqa: F401
from ai_analytics_agent.embeddings.embedding_utils import (
    build_embedding_text,
    vector_to_pg,
)
from ai_analytics_agent.metadata_db import get_connection, close_pool

# --------------------------------------------------
# Initialize database:
# Create pgvector extension + table
# --------------------------------------------------
embedding_model = SentenceTransformer(config.settings.EMBEDDING_MODEL)

# Build rows for insertion
rows = []

for model in models:
    text = build_embedding_text("model", model)
    embedding = embedding_model.encode(text).tolist()

    rows.append(
        ("model", model["model_name"], json.dumps(model), vector_to_pg(embedding))
    )

for rel in relationships:
    text = build_embedding_text("relationship", rel)
    embedding = embedding_model.encode(text).tolist()

    rows.append(
        (
            "relationship",
            f"{rel['source_model']}->{rel['target_model']}",
            json.dumps(rel),
            vector_to_pg(embedding),
        )
    )

for metric in metrics:
    text = build_embedding_text("metric", metric)
    embedding = embedding_model.encode(text).tolist()

    rows.append(
        ("metric", metric["metric_name"], json.dumps(metric), vector_to_pg(embedding))
    )


# Automatically borrows and returns connection
with get_connection() as conn:
    with conn.cursor() as cursor:

        # cursor.execute("""
        # CREATE EXTENSION IF NOT EXISTS vector;
        # """)

        # cursor.execute(f"""
        # CREATE TABLE IF NOT EXISTS schema_embeddings (
        #     id BIGSERIAL PRIMARY KEY,
        #     entity_type TEXT NOT NULL,
        #     entity_name TEXT NOT NULL,
        #     metadata JSONB NOT NULL,
        #     embedding VECTOR({settings.EMBEDDING_DIMENSION})
        # );
        # """)

        # print(f"Thread {threading.current_thread().name} done")

        # conn.commit()

        # --------------------------------------------------
        # Bulk insert
        # --------------------------------------------------

        execute_values(
            cursor,
            """
            INSERT INTO schema_embeddings (
                entity_type,
                entity_name,
                metadata,
                embedding
            )
            VALUES %s
            """,
            rows,
        )

        conn.commit()

        print(f"Inserted {len(rows)} embedding rows")
