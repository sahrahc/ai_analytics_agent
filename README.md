# Semantic SQL Agent

AI-powered semantic analytics platform that converts natural language metric requests into validated Snowflake SQL using dbt metadata, LangGraph orchestration, and OpenAI APIs.

Next Steps:
1. Intent parser LLM call for more sophisticated requests (dependent on business glossary)
2. Conditional validations, looping back to SQL processing upon failure (once)
3. Human-in-the-loop to review final validation and cost estimates
4. Execute SQL

Additional Steps
1. Fixtures
2. Increase unit test coverage
---

# Features

1 of 2 Pre-processing Semantic Metadata

* Parse dbt semantic metadata from:

  * `manifest.json`
  * `catalog.json`
  * semantic YAML files (`facts.yml`, `dimensions.yml`)
* Extract:

  * models (entities)
  * dimensions
  * metrics
  * PK/FK relationships
  * lineage

* Load:
  * build embedding vector
  * load into postgres metadata database

2 of 2 Agent

* Extract intent from English prompt (in progress)
* Embedding vector search against intent
* Generate Snowflake SQL 
* LangGraph orchestration pipeline
* Semantic validation using parsed metadata
* SQL validation using:
  * sqlglot
* Validation and performance via `EXPLAIN` against live Snowflake database
* Metric documentation generation
* Prompt versioning support

---

# Architecture

```text
User Request
    ↓
LangGraph Workflow
    ↓
Semantic Retrieval
    ↓
OpenAI Responses API
    ↓
SQL Generation
    ↓
Semantic Validation
    ↓
Snowflake Validation
```

---

# Project Structure

```text
project/
├── config.py
├── metadata_db.py
├── graph.py
├── state.py
├── main.py
├── embeddings/
│   ├── embedding_loader.py
│   ├── embedding_utils.py
│   ├── vector_store.py
├── prompts/
│   ├── build_prompt.py
│   └── prompt_template.py
├── metadata/
│   ├── load_metadata.py
│   ├── semantic_data.py
├── agents/
│   ├── generate_sql.py
├── validation/
│   ├── validate_static_sql.py
│   ├── validate_semantic_sql.py
│   ├── validate_database.py

(preprocessing)

├── metadata_registry/
│   ├── parse_semantic_context.py
│   ├── parse_semantic_model_facts.py
├── input/
├── output/

(tests)

├── tests/
│   ├── conftest.py
(one test subdirectory for every project subdirectory)

└── README.md
```

---

# Requirements (see pyproject.toml for full list)

```bash
uv add openai
uv add langgraph
uv add sqlglot
uv add pyyaml
uv add snowflake-connector-python
uv add pgvector
uv add psycopg2-binary
uv add rapidfuzz
```

# Other setup
```bash
brew install postgresql@18
```

---

# Environment Variables

```bash
export OPENAI_API_KEY="YOUR_API_KEY"
```

Snowflake:

```bash
export SNOWFLAKE_ACCOUNT="ACCOUNT"
export SNOWFLAKE_USER="USER"
export SNOWFLAKE_WAREHOUSE="WAREHOUSE"
export SNOWFLAKE_DATABASE="DATABASE"
export SNOWFLAKE_SCHEMA="SCHEMA"
export PRIVATE_KEY_PATH="SNOWFLAKE_PRIVATE_KEY_PATH"
export PRIVATE_KEY_PASSPHRASE="SNOWFLAKE_PRIVATE_KEY_PASSPHRASE"
```

---

# Running the dbt json/yaml parsers
```bash
uv run embeddings/parse_semantic_context.py
uv run embeddings/parse_semantic_model_context.py
```

```bash
uv run embeddings/embedding_loader.py
```
# Running the SQL Agent with example input

```bash
uv -run main.py "Find historical roas by week"
```

Example output:

```sql
SELECT
  c.year AS year,
  c.week AS week,
  SUM(f.revenue_usd) AS revenue_usd_weekly,
  SUM(f.cost_usd) AS cost_usd_weekly,
  CASE
    WHEN SUM(f.cost_usd) = 0 THEN NULL
    ELSE SUM(f.revenue_usd) / NULLIF(SUM(f.cost_usd), 0)
  END AS roas_weekly
FROM STREAMING_ADS.streaming_ads_schema.fct_campaign_daily f
JOIN STREAMING_ADS.streaming_ads_schema.dim_calendar c
  ON f.date_key = c.date_key
GROUP BY
  c.year,
  c.week
ORDER BY
  c.year,
  c.week;
```

---
# Metadata Registry Workflow
```text
parse_semantic_context (entities from manifest + catalog)
    ↓
parse_semantic_model_facts (relationships and metrics from facts.yml)
    ↓
create_vector_embeddings
    ↓
load_embeddings
```

# LangGraph Workflow

Current workflow:

```text
embedding_vector_search
    ↓
build_prompt
    ↓
generate_sql
    ↓
validate_sql
```

---

# OpenAI Integration

Uses the OpenAI Responses API:

```python
client.responses.create(...)
```

Endpoint:

```text
POST https://api.openai.com/v1/responses
```

Features:

* structured JSON outputs
* reasoning-enabled prompts
* prompt templating/versioning
* semantic SQL generation

---

# Semantic Validation

Validation layers:

1. SQL syntax validation using `sqlglot`
2. Semantic model validation
3. Join validation
4. Column validation
5. Performance of query plan from Snowflake `EXPLAIN` 

Example:

```python
sqlglot.parse_one(sql, dialect="snowflake")
```

---

# Snowflake Validation

Optional lightweight warehouse validation:

```sql
EXPLAIN USING TEXT
SELECT ...
```

Purpose:

* validate schema references
* validate joins
* detect execution issues
* detect performance issues
*

---

# Metric Documentation Generation

The project can generate:

* business summaries
* lineage
* source models
* source columns
* relationship mappings

Example:

```json
{
  "metric_name": "roas",
  "summary": "Return on Ad Spend measures advertising efficiency.",
  "lineage": {
    "source_model": "fct_campaign_daily"
  }
}
```

---

# Prompt Versioning

Prompt templates are versioned for reproducibility.

Example:

```python
PROMPT_VERSION = "v1"
```

Supports:

* A/B testing
* rollback
* experimentation
* evaluation

---

# Future Enhancements

## Phase 2

* pgvector retrieval
* embedding-based metric discovery
* conversational analytics

---

---

# Example Queries

"Find historical roas summarized by week"

---

# License

MIT
