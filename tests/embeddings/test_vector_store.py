# tests/test_vector_store.py

from unittest.mock import MagicMock
from ai_analytics_agent.embeddings.embedding_utils import vector_to_pg


def test_vector_to_pg():

    vector = [0.1, 0.2, 0.3]

    result = vector_to_pg(vector)

    assert result == "[0.1,0.2,0.3]"
