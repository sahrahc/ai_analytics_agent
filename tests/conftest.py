import pytest

# Fixtures for testing embedding search


@pytest.fixture
def test_models():

    return [
        {
            "name": "fct_ad_sessions",
            "description": "Fact table for ad playback sessions",
            "columns": [
                {"name": "session_id"},
                {"name": "country_id"},
                {"name": "event_date"},
                {"name": "ad_count"},
            ],
        }
    ]


@pytest.fixture
def test_relationships():

    return [
        {
            "from_model": "fct_ad_sessions",
            "to_model": "dim_country",
            "from_column": "country_id",
            "relationship_type": "many_to_one",
            # "dimensions": ["country"],
        }
    ]


@pytest.fixture
def test_metrics():

    return [
        {
            "metric_name": "ad_load",
            "model": "fct_ad_sessions",
            "aggregation": "AVG",
            "expression": "ad_count",
            "dimensions": ["country"],
            # "time_dimensions": ["event_date"],
        }
    ]


@pytest.fixture
def sample_intent():

    return {
        "metrics": ["ad_load"],
        "dimensions": ["country"],
        "filters": [],
        "time_grain": "month",
        "start_date": None,
        "end_date": None,
        "ranking": None,
        "limit": None,
        "analysis_type": "trend",
    }
