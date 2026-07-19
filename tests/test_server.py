import asyncio

import server


def test_registers_expected_public_tools():
    tools = asyncio.run(server.list_tools())
    names = {tool.name for tool in tools}

    assert names == {
        "search_knowledge",
        "get_case_study",
        "get_mythology",
        "get_template",
        "get_methodology",
        "generate_worldbuilding_prompt",
        "analyze_power_system",
        "generate_character",
        "generate_plot",
        "analyze_writing",
        "suggest_titles",
        "generate_dialogue",
    }


def test_partial_genre_uses_matching_title_pattern():
    response = server._handle_suggest_titles({"genre": "玄幻", "theme": "命运"})

    assert response[0].text.startswith("标题推荐：")
    assert "命运" in response[0].text


def test_empty_search_query_returns_guidance():
    response = server._handle_search({}, {"query": ""})

    assert response[0].text == "请提供搜索关键词"
