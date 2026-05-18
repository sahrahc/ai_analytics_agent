# rom unittest.mock import patch
from ai_analytics_agent.prompts.build_prompt import build_prompt

test1 = "historical ad load by country"
test2 = "Find historical roas summarized by week"


def test_build_prompt():

    metadata = [{"entity_type": "metric", "entity_name": "ad_load"}]

    system_prompt, user_prompt = build_prompt(
        analysis_request=test1, metadata_results=metadata
    )

    assert "analytics engineer" in system_prompt

    assert "historical ad load" in user_prompt

    assert "ad_load" in user_prompt

    #  Find historical roas summarized by week
