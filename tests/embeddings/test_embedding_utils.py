# tests/test_embedding_utils.py

from ai_analytics_agent.embeddings.embedding_utils import build_embedding_text


def test_build_embedding_text_model(test_models):

    model = test_models[0]

    result = build_embedding_text(entity_type="model", payload=model)

    assert "fct_ad_sessions" in result
    assert "ad playback sessions" in result
    assert "session_id" in result
    assert "country_id" in result


def test_build_embedding_text_relationship(test_relationships):

    relationship = test_relationships[0]

    result = build_embedding_text(entity_type="relationship", payload=relationship)

    assert "fct_ad_sessions" in result
    assert "dim_country" in result
    assert "country_id" in result


def test_build_embedding_text_metric(test_metrics):

    metric = test_metrics[0]

    result = build_embedding_text(entity_type="metric", payload=metric)

    assert "ad_load" in result
