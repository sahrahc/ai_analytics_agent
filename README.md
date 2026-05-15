# Semantic SQL Agent

AI-powered semantic analytics platform that converts natural language metric requests into validated Snowflake SQL using dbt metadata, LangGraph orchestration, and OpenAI APIs.

---

# Features

* Parse dbt semantic metadata from:

  * `manifest.json`
  * `catalog.json`
  * semantic YAML files
* Extract:

  * models
  * dimensions
  * metrics
  * PK/FK relationships
  * lineage
* Generate Snowflake SQL from English prompts
* LangGraph orchestration pipeline
* Semantic validation using parsed metadata
* SQL validation using:

  * sqlglot
  * Snowflake `EXPLAIN`
* Metric documentation generation
* Prompt versioning support
* Extensible architecture for pgvector retrieval

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
Optional Snowflake Validation
```

---

# Project Structure

```text
project/
├── clients.py
├── graph.py
├── generate_sql.py
├── parse_metrics.py
├── parse_relationships.py
├── validate_sql.py
├── generate_metric_docs.py
├── semantic_model.json
├── metrics.json
├── prompts/
│   ├── system_prompts.py
│   └── user_prompts.py
└── README.md
```

---

# Requirements (see pyproject.toml for full list)

```bash
pip install openai
pip install langgraph
pip install sqlglot
pip install pyyaml
pip install snowflake-connector-python
pip install pgvector
pip install psycopg2-binary
```

---

# Environment Variables

```bash
export OPENAI_API_KEY="YOUR_API_KEY"
```

Optional Snowflake:

```bash
export SNOWFLAKE_ACCOUNT="ACCOUNT"
export SNOWFLAKE_USER="USER"
export SNOWFLAKE_PASSWORD="PASSWORD"
export SNOWFLAKE_WAREHOUSE="WAREHOUSE"
export SNOWFLAKE_DATABASE="DATABASE"
export SNOWFLAKE_SCHEMA="SCHEMA"
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
    SUM(revenue_usd) / NULLIF(SUM(cost_usd), 0) AS roas
FROM fct_campaign_daily
```

---
# Metadata Registry Workflow
```text
parse_dbt_manifest_catalog
    ↓
parse_dbt_fact_semantic
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
5. Optional Snowflake `EXPLAIN`

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
* avoid full query execution

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

# Recommended Stack

| Component      | Technology            |
| -------------- | --------------------- |
| Orchestration  | LangGraph             |
| LLM            | OpenAI GPT-5 API      |
| Embeddings     | OpenAI Embeddings API |
| Warehouse      | Snowflake             |
| Validation     | sqlglot               |
| Semantic Store | PostgreSQL            |
| Vector Search  | pgvector              |

---

# Example End-to-End Flow

```text
"Which campaigns have the best marketing efficiency?"
        ↓
Metric Retrieval
        ↓
Semantic Context Retrieval
        ↓
OpenAI SQL Generation
        ↓
Semantic Validation
        ↓
Snowflake EXPLAIN
        ↓
Validated SQL
```

---

# License

MIT
