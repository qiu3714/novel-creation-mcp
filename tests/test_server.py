import asyncio

import pytest

import server


PUBLIC_TOOL_CASES = [
    ("search_knowledge", {"query": "角色"}),
    ("get_case_study", {"title": "不存在的案例"}),
    ("get_mythology", {"culture": "希腊神话"}),
    ("get_template", {"template_type": "力量体系"}),
    ("get_methodology", {"topic": "角色塑造"}),
    ("generate_worldbuilding_prompt", {"world_type": "修仙世界"}),
    ("analyze_power_system", {"system_description": "灵气分层，需要资源突破"}),
    ("generate_character", {"archetype": "主角", "genre": "玄幻"}),
    ("generate_plot", {"plot_type": "三幕结构", "genre": "悬疑"}),
    ("analyze_writing", {"text": "伏笔"}),
    ("suggest_titles", {"genre": "玄幻", "theme": "命运"}),
    ("generate_dialogue", {"scenario": "冲突对话"}),
]


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


@pytest.mark.parametrize(("tool_name", "arguments"), PUBLIC_TOOL_CASES)
def test_public_tools_return_text_content(tool_name, arguments):
    response = asyncio.run(server.call_tool(tool_name, arguments))

    assert response
    assert response[0].type == "text"
    assert response[0].text


def test_call_tool_accepts_missing_argument_mapping():
    response = asyncio.run(server.call_tool("generate_character", None))

    assert "角色设定模板：主角" in response[0].text


def test_search_coerces_non_string_query():
    response = server._handle_search(
        {"test_section": {"example": "123"}},
        {"query": 123, "section": "test_section"},
    )

    assert "找到 1 条相关内容" in response[0].text
