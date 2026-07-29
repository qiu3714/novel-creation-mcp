"""
小说创作MCP工具 - MCP服务器
===========================

提供小说创作相关的MCP工具，包括：
- search_knowledge: 搜索知识库
- get_case_study: 获取案例分析
- get_mythology: 获取神话传说素材
- get_template: 获取写作模板
- get_methodology: 获取写作方法论
- generate_worldbuilding_prompt: 生成世界观构建提示词
- analyze_power_system: 分析力量体系
- generate_character: 生成角色设定
- generate_plot: 生成情节设计
- analyze_writing: 分析写作技法
- suggest_titles: 推荐小说标题
- generate_dialogue: 生成对话模板
"""

import json
import random
import re
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from novel_data import (
    PLOT_TYPES, CLASSIFICATION_MAPPING, WRITING_METHODOLOGY,
    TECHNIQUE_TERMINOLOGY, WORLD_TEMPLATES, CHARACTER_ARCHETYPES,
    DIALOGUE_TEMPLATES, TITLE_PATTERNS, CONTENT_CLASSIFICATION_KEYWORDS
)

# ============================================================
# 知识库懒加载缓存
# ============================================================

_kb_cache = None
_collected_cache = None
_cache_loaded = False

KB_FILE = Path(__file__).parent / "knowledge" / "knowledge-base.json"
COLLECTED_FILE = Path(__file__).parent / "knowledge" / "collected_content.json"


def load_main_knowledge():
    global _kb_cache
    if _kb_cache is None:
        try:
            with open(KB_FILE, "r", encoding="utf-8") as f:
                _kb_cache = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            _kb_cache = {}
    return _kb_cache


def load_collected_content():
    global _collected_cache
    if _collected_cache is None:
        try:
            with open(COLLECTED_FILE, "r", encoding="utf-8") as f:
                _collected_cache = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            _collected_cache = {"metadata": {}, "collected_content": []}
    return _collected_cache


def _get_collected_items(collected):
    if not isinstance(collected, dict):
        return []
    items = collected.get("collected_content")
    if items is None:
        items = collected.get("content", [])
    return items if isinstance(items, list) else []


def _get_collected_item_key(item):
    if not isinstance(item, dict):
        return str(item)
    return item.get("id") or item.get("title") or str(item)


def load_knowledge():
    global _cache_loaded
    kb = load_main_knowledge()
    if not _cache_loaded:
        collected = load_collected_content()
        collected_items = _get_collected_items(collected)
        if collected_items:
            if "collected_content" not in kb:
                kb["collected_content"] = []
            existing_keys = {_get_collected_item_key(item) for item in kb.get("collected_content", [])}
            new_items = [item for item in collected_items if _get_collected_item_key(item) not in existing_keys]
            if new_items:
                kb["collected_content"].extend(new_items)
        _cache_loaded = True
    return kb


def reload_cache():
    global _kb_cache, _collected_cache, _cache_loaded
    _kb_cache = None
    _collected_cache = None
    _cache_loaded = False
    return load_knowledge()


def get_cache_info():
    return {
        "main_kb_cached": _kb_cache is not None,
        "collected_cached": _collected_cache is not None,
        "main_kb_sections": list(_kb_cache.keys()) if _kb_cache else [],
        "collected_count": len(_get_collected_items(_collected_cache)) if _collected_cache else 0
    }


# ============================================================
# 通用搜索辅助
# ============================================================

def _normalize_arguments(arguments):
    return arguments if isinstance(arguments, dict) else {}


def _get_text_argument(arguments, key, default=""):
    value = _normalize_arguments(arguments).get(key, default)
    if value is None:
        return default
    text = str(value).strip()
    return text if text else default


def _search_in_data(data, query, path=""):
    query_text = str(query).lower()
    if not query_text:
        return []

    results = []
    if isinstance(data, dict):
        for k, v in data.items():
            current_path = f"{path}.{k}" if path else k
            if isinstance(v, str):
                if query_text in k.lower() or query_text in v.lower():
                    results.append({"path": current_path, "content": v[:200]})
            elif isinstance(v, (dict, list)):
                results.extend(_search_in_data(v, query, current_path))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            current_path = f"{path}[{i}]"
            if isinstance(item, str):
                if query_text in item.lower():
                    results.append({"path": current_path, "content": item[:200]})
            elif isinstance(item, dict):
                title = item.get("title", item.get("name", ""))
                content = item.get("content", item.get("summary", item.get("description", "")))
                if query_text in str(title).lower() or query_text in str(content).lower():
                    results.append({
                        "path": current_path,
                        "title": title,
                        "content": str(content)[:200],
                        "type": item.get("type", "未知")
                    })
                elif isinstance(content, (dict, list)):
                    results.extend(_search_in_data(content, query, current_path))
            elif isinstance(item, (dict, list)):
                results.extend(_search_in_data(item, query, current_path))
    return results


# ============================================================
# 内容分类辅助
# ============================================================

def _classify_content(text):
    text_lower = text.lower()
    scores = {}
    for section, keywords in CLASSIFICATION_MAPPING.items():
        if keywords in scores:
            scores[keywords] += 1
        else:
            scores[keywords] = 0
        if section in text_lower:
            scores[keywords] += 1
    for section, kw_data in CONTENT_CLASSIFICATION_KEYWORDS.items():
        score = 0
        for kw in kw_data.get("primary", []):
            if kw in text_lower:
                score += 3
        for kw in kw_data.get("secondary", []):
            if kw in text_lower:
                score += 1
        if score > 0:
            scores[section] = scores.get(section, 0) + score
    if scores:
        best = max(scores, key=scores.get)
        if scores[best] > 0:
            return best
    return "summary"


# ============================================================
# MCP 服务器初始化
# ============================================================

app = Server("novel-creation-mcp")


@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="search_knowledge",
            description="搜索小说创作知识库，查找相关的写作技巧、案例分析、方法论等内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词，如'角色塑造'、'情节设计'、'世界观构建'等"
                    },
                    "section": {
                        "type": "string",
                        "description": "指定搜索的知识库分区（可选）：character_design, plot_structure, worldbuilding, writing_techniques, dialogue_generation, mythology, templates, genresearch, platform_guides, monetization"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_case_study",
            description="获取经典网文案例分析，包括成功要素、写作技巧、可借鉴之处等",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "小说标题，如'斗破苍穹'、'全职高手'、'庆余年'等"
                    }
                },
                "required": ["title"]
            }
        ),
        Tool(
            name="get_mythology",
            description="获取神话传说素材，用于世界观构建和角色设计",
            inputSchema={
                "type": "object",
                "properties": {
                    "culture": {
                        "type": "string",
                        "description": "神话体系：中国神话、北欧神话、希腊神话、日本神话、印度神话等"
                    }
                },
                "required": ["culture"]
            }
        ),
        Tool(
            name="get_template",
            description="获取万能写作模板，包括情节模板、角色模板、世界观模板等",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_type": {
                        "type": "string",
                        "description": "模板类型：情节模板、角色模板、世界观模板、开篇模板、高潮模板等"
                    }
                },
                "required": ["template_type"]
            }
        ),
        Tool(
            name="get_methodology",
            description="获取写作方法论，系统化的创作指导",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "方法论主题：角色塑造、情节设计、世界观构建、对话写作、开篇设计、爽点设计等"
                    }
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="generate_worldbuilding_prompt",
            description="根据指定类型生成世界观构建的详细提示词",
            inputSchema={
                "type": "object",
                "properties": {
                    "world_type": {
                        "type": "string",
                        "description": "世界观类型：修仙世界、玄幻世界、都市世界、末日世界、游戏世界"
                    }
                },
                "required": ["world_type"]
            }
        ),
        Tool(
            name="analyze_power_system",
            description="分析力量体系的设计，提供优化建议",
            inputSchema={
                "type": "object",
                "properties": {
                    "system_description": {
                        "type": "string",
                        "description": "力量体系的描述"
                    }
                },
                "required": ["system_description"]
            }
        ),
        Tool(
            name="generate_character",
            description="生成角色设定模板",
            inputSchema={
                "type": "object",
                "properties": {
                    "archetype": {
                        "type": "string",
                        "description": "角色原型：主角、反派、导师、配角"
                    },
                    "genre": {
                        "type": "string",
                        "description": "小说类型：玄幻、都市、科幻、悬疑等"
                    }
                },
                "required": ["archetype"]
            }
        ),
        Tool(
            name="generate_plot",
            description="生成情节设计模板",
            inputSchema={
                "type": "object",
                "properties": {
                    "plot_type": {
                        "type": "string",
                        "description": "情节类型：英雄之旅、三幕结构、起承转合、多线并行、倒叙揭秘"
                    },
                    "genre": {
                        "type": "string",
                        "description": "小说类型"
                    }
                },
                "required": ["plot_type"]
            }
        ),
        Tool(
            name="analyze_writing",
            description="分析写作技法，提供术语解释和技巧建议",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "要分析的文本或技法术语"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="suggest_titles",
            description="根据小说类型和主题推荐标题",
            inputSchema={
                "type": "object",
                "properties": {
                    "genre": {
                        "type": "string",
                        "description": "小说类型：玄幻仙侠、都市现实、游戏竞技、悬疑推理等"
                    },
                    "theme": {
                        "type": "string",
                        "description": "小说主题关键词"
                    }
                },
                "required": ["genre"]
            }
        ),
        Tool(
            name="generate_dialogue",
            description="生成对话模板和技巧",
            inputSchema={
                "type": "object",
                "properties": {
                    "scenario": {
                        "type": "string",
                        "description": "对话场景：冲突对话、情感对话、权谋对话、日常对话、战斗对话"
                    }
                },
                "required": ["scenario"]
            }
        )
    ]


# ============================================================
# 工具处理器
# ============================================================

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    arguments = _normalize_arguments(arguments)
    kb = load_knowledge()

    if name == "search_knowledge":
        return _handle_search(kb, arguments)
    elif name == "get_case_study":
        return _handle_case_study(kb, arguments)
    elif name == "get_mythology":
        return _handle_mythology(kb, arguments)
    elif name == "get_template":
        return _handle_template(kb, arguments)
    elif name == "get_methodology":
        return _handle_methodology(arguments)
    elif name == "generate_worldbuilding_prompt":
        return _handle_worldbuilding(arguments)
    elif name == "analyze_power_system":
        return _handle_power_system(arguments)
    elif name == "generate_character":
        return _handle_character(arguments)
    elif name == "generate_plot":
        return _handle_plot(arguments)
    elif name == "analyze_writing":
        return _handle_analyze_writing(arguments)
    elif name == "suggest_titles":
        return _handle_suggest_titles(arguments)
    elif name == "generate_dialogue":
        return _handle_dialogue(arguments)
    else:
        return [TextContent(type="text", text=f"未知工具: {name}")]


# ============================================================
# search_knowledge
# ============================================================

def _normalize_collected_item(item):
    if not isinstance(item, dict):
        return None

    content = item.get("content")
    if isinstance(content, dict):
        title = content.get("title") or item.get("title") or ""
        summary = (
            content.get("summary")
            or content.get("content_summary")
            or content.get("description")
            or ""
        )
        content_type = item.get("content_type") or content.get("content_type") or content.get("type") or ""
        search_text = f"{title} {summary} {content} {item.get('section', '')} {content_type}"
    else:
        title = item.get("title", "")
        summary = item.get("content_summary") or item.get("summary") or item.get("description") or ""
        content_type = item.get("content_type") or item.get("type") or ""
        search_parts = [
            title,
            summary,
            item.get("section", ""),
            content_type,
            item.get("platform", ""),
            item.get("source_reference", ""),
            item.get("key_points", ""),
            item.get("keywords", ""),
        ]
        search_text = " ".join(str(part) for part in search_parts)

    return {
        "path": f"collected_content.{item.get('id', '')}",
        "title": title,
        "content": str(summary)[:200],
        "type": content_type,
        "section": item.get("section"),
        "search_text": search_text,
    }


def _search_collected_items(items, query, section=None):
    query_text = query.lower()
    results = []
    for item in items:
        normalized = _normalize_collected_item(item)
        if not normalized:
            continue
        if section:
            item_section = normalized.get("section")
            if item_section and item_section != section:
                continue
            if not item_section and _classify_content(normalized["search_text"]) != section:
                continue
        if query_text in normalized["search_text"].lower():
            results.append({
                "path": normalized["path"],
                "title": normalized["title"],
                "content": normalized["content"],
                "type": normalized["type"],
            })
    return results


def _handle_search(kb, arguments):
    query = _get_text_argument(arguments, "query")
    section = _get_text_argument(arguments, "section", None)

    if not query:
        return [TextContent(type="text", text="请提供搜索关键词")]

    results = []
    if section:
        if section in kb:
            results.extend(_search_in_data(kb[section], query, section))
        results.extend(_search_collected_items(kb.get("collected_content", []), query, section))
    else:
        for key in kb:
            if key == "collected_content":
                continue
            results.extend(_search_in_data(kb[key], query, key))
        results.extend(_search_collected_items(kb.get("collected_content", []), query))

    if not results:
        return [TextContent(type="text", text=f"未找到与'{query}'相关的内容。请尝试其他关键词。")]

    output = f"搜索结果：'{query}'\n找到 {len(results)} 条相关内容\n\n"
    for i, r in enumerate(results[:10], 1):
        output += f"{i}. 【{r.get('path', '')}】\n"
        if r.get("title"):
            output += f"   标题：{r['title']}\n"
        if r.get("type"):
            output += f"   类型：{r['type']}\n"
        if r.get("content"):
            output += f"   内容：{r['content']}\n"
        output += "\n"

    return [TextContent(type="text", text=output)]


# ============================================================
# get_case_study
# ============================================================

def _handle_case_study(kb, arguments):
    title = _get_text_argument(arguments, "title")
    if not title:
        return [TextContent(type="text", text="请提供小说标题")]

    ip_studies = kb.get("ip_case_studies", {})
    case = None
    for key, value in ip_studies.items():
        if isinstance(value, dict):
            if value.get("title") == title or title in key:
                case = value
                break
            for item_key, item_value in value.items():
                if isinstance(item_value, dict) and (item_value.get("title") == title or title in item_key):
                    case = item_value
                    break

    if not case:
        collected = kb.get("collected_content", [])
        for item in collected:
            content = item.get("content", {})
            if content.get("title") == title or title in str(content):
                case = content
                break

    if not case:
        return [TextContent(type="text", text=f"未找到'{title}'的案例分析。请检查标题是否正确。")]

    output = f"案例分析：{title}\n\n"
    if isinstance(case, dict):
        for key, value in case.items():
            if isinstance(value, list):
                output += f"【{key}】\n"
                for item in value:
                    output += f"  • {item}\n"
                output += "\n"
            elif isinstance(value, dict):
                output += f"【{key}】\n"
                for k, v in value.items():
                    output += f"  {k}: {v}\n"
                output += "\n"
            else:
                output += f"【{key}】{value}\n\n"
    else:
        output += str(case)

    return [TextContent(type="text", text=output)]


# ============================================================
# get_mythology
# ============================================================

def _handle_mythology(kb, arguments):
    culture = _get_text_argument(arguments, "culture")
    if not culture:
        return [TextContent(type="text", text="请提供神话体系名称")]

    mythology = kb.get("mythology", {})
    result = None
    for key, value in mythology.items():
        if culture in key or (isinstance(value, dict) and culture in str(value)):
            result = {key: value}
            break

    if not result:
        collected = kb.get("collected_content", [])
        myth_items = [item for item in collected if item.get("section") == "mythology"]
        for item in myth_items:
            content = item.get("content", {})
            if culture in str(content):
                result = content
                break

    if not result:
        return [TextContent(type="text", text=f"未找到'{culture}'的神话素材。请检查名称是否正确。")]

    output = f"神话素材：{culture}\n\n"
    if isinstance(result, dict):
        for key, value in result.items():
            if isinstance(value, dict):
                output += f"【{key}】\n"
                for k, v in value.items():
                    if isinstance(v, list):
                        output += f"  {k}:\n"
                        for item in v:
                            output += f"    • {item}\n"
                    else:
                        output += f"  {k}: {v}\n"
                output += "\n"
            elif isinstance(value, list):
                output += f"【{key}】\n"
                for item in value:
                    output += f"  • {item}\n"
                output += "\n"
            else:
                output += f"【{key}】{value}\n\n"
    else:
        output += str(result)

    return [TextContent(type="text", text=output)]


# ============================================================
# get_template
# ============================================================

def _handle_template(kb, arguments):
    template_type = _get_text_argument(arguments, "template_type")
    if not template_type:
        return [TextContent(type="text", text="请提供模板类型")]

    matched_section = _classify_content(template_type)
    templates = kb.get("templates", {})
    result = None
    for key, value in templates.items():
        if template_type in key or (isinstance(value, dict) and template_type in str(value)):
            result = {key: value}
            break
    if not result and matched_section in templates:
        result = {matched_section: templates[matched_section]}
    if not result:
        for key, value in templates.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if template_type in sub_key or template_type in str(sub_value):
                        result = {f"{key}.{sub_key}": sub_value}
                        break

    if not result:
        collected = kb.get("collected_content", [])
        template_items = [item for item in collected if item.get("content_type") in ["模板", "公式"]]
        for item in template_items:
            content = item.get("content", {})
            if template_type in str(content):
                result = content
                break

    if not result:
        return [TextContent(type="text", text=f"未找到'{template_type}'的模板。请检查类型是否正确。")]

    output = f"写作模板：{template_type}\n\n"
    if isinstance(result, dict):
        for key, value in result.items():
            if isinstance(value, dict):
                output += f"【{key}】\n"
                for k, v in value.items():
                    if isinstance(v, list):
                        output += f"  {k}:\n"
                        for item in v:
                            output += f"    • {item}\n"
                    elif isinstance(v, dict):
                        output += f"  {k}:\n"
                        for kk, vv in v.items():
                            output += f"    {kk}: {vv}\n"
                    else:
                        output += f"  {k}: {v}\n"
                output += "\n"
            elif isinstance(value, list):
                output += f"【{key}】\n"
                for item in value:
                    output += f"  • {item}\n"
                output += "\n"
            else:
                output += f"【{key}】{value}\n\n"
    else:
        output += str(result)

    return [TextContent(type="text", text=output)]


# ============================================================
# get_methodology
# ============================================================

def _handle_methodology(arguments):
    topic = _get_text_argument(arguments, "topic")
    if not topic:
        available = ", ".join(WRITING_METHODOLOGY.keys())
        return [TextContent(type="text", text=f"可用方法论主题：{available}")]

    matched = None
    for key in WRITING_METHODOLOGY:
        if topic in key or key in topic:
            matched = key
            break

    if not matched:
        available = ", ".join(WRITING_METHODOLOGY.keys())
        return [TextContent(type="text", text=f"未找到'{topic}'的方法论。可用主题：{available}")]

    data = WRITING_METHODOLOGY[matched]
    output = f"写作方法论：{matched}\n{data['description']}\n\n"
    output += "【核心原则】\n"
    for p in data["principles"]:
        output += f"  • {p}\n"
    output += "\n【具体方法】\n"
    for i, m in enumerate(data["methods"], 1):
        output += f"  {i}. {m}\n"
    output += "\n【常见误区】\n"
    for m in data["common_mistakes"]:
        output += f"  ✗ {m}\n"
    output += "\n【经典案例】\n"
    for e in data["examples"]:
        output += f"  ★ {e}\n"

    return [TextContent(type="text", text=output)]


# ============================================================
# generate_worldbuilding_prompt
# ============================================================

def _handle_worldbuilding(arguments):
    world_type = _get_text_argument(arguments, "world_type")
    if not world_type:
        available = ", ".join(WORLD_TEMPLATES.keys())
        return [TextContent(type="text", text=f"可用世界观类型：{available}")]

    template = WORLD_TEMPLATES.get(world_type)
    if not template:
        for key in WORLD_TEMPLATES:
            if world_type in key or key in world_type:
                template = WORLD_TEMPLATES[key]
                world_type = key
                break

    if not template:
        available = ", ".join(WORLD_TEMPLATES.keys())
        return [TextContent(type="text", text=f"未找到'{world_type}'的世界观模板。可用类型：{available}")]

    prompt = f"请构建一个完整的{world_type}世界观，包含以下核心要素：\n\n"
    prompt += "【核心设定要素】\n"
    for element in template["core_elements"]:
        prompt += f"  • {element}\n"
    prompt += f"\n【力量体系基础】{template['power_system']}\n"
    prompt += "\n【典型场景设定】\n"
    for setting in template["typical_settings"]:
        prompt += f"  • {setting}\n"
    prompt += "\n【冲突来源】\n"
    for conflict in template["conflict_sources"]:
        prompt += f"  • {conflict}\n"
    prompt += "\n【构建要求】\n"
    prompt += "  1. 所有设定需要内在逻辑一致\n"
    prompt += "  2. 力量体系需要有明确的等级和代价\n"
    prompt += "  3. 历史背景需要与当前世界状态呼应\n"
    prompt += "  4. 需要考虑不同势力之间的平衡关系\n"
    prompt += "  5. 预留足够的扩展空间"

    return [TextContent(type="text", text=prompt)]


# ============================================================
# analyze_power_system
# ============================================================

def _handle_power_system(arguments):
    desc = _get_text_argument(arguments, "system_description")
    if not desc:
        return [TextContent(type="text", text="请提供力量体系描述")]

    analysis = f"力量体系分析\n{'=' * 40}\n\n"
    analysis += f"原始描述：{desc[:200]}\n\n"
    analysis += "【评估维度】\n\n"
    analysis += "1. 等级划分\n"
    analysis += "   - 是否有清晰的等级划分？\n"
    analysis += "   - 等级之间的差距是否合理？\n"
    analysis += "   - 等级提升的条件是否明确？\n\n"
    analysis += "2. 力量来源\n"
    analysis += "   - 力量的来源是什么？（灵气/魔力/科技/异能）\n"
    analysis += "   - 力量来源是否有统一的底层逻辑？\n"
    analysis += "   - 不同力量类型之间是否平衡？\n\n"
    analysis += "3. 代价机制\n"
    analysis += "   - 使用力量需要付出什么代价？\n"
    analysis += "   - 代价是否与力量强度成正比？\n"
    analysis += "   - 是否有不可逆的代价？\n\n"
    analysis += "4. 成长路径\n"
    analysis += "   - 主角的成长路径是否清晰？\n"
    analysis += "   - 是否有捷径和瓶颈？\n"
    analysis += "   - 成长速度是否合理？\n\n"
    analysis += "5. 战斗表现\n"
    analysis += "   - 不同等级的战斗表现差距如何？\n"
    analysis += "   - 是否有以弱胜强的可能？\n"
    analysis += "   - 战斗描写是否有视觉冲击力？\n\n"
    analysis += "【优化建议】\n"
    analysis += "  1. 确保力量体系有统一的底层逻辑\n"
    analysis += "  2. 设计合理的代价机制，避免力量膨胀\n"
    analysis += "  3. 留出以弱胜强的空间，增加戏剧性\n"
    analysis += "  4. 考虑力量体系与世界观的融合\n"
    analysis += "  5. 避免过于复杂，保持读者可理解性"

    return [TextContent(type="text", text=analysis)]


# ============================================================
# generate_character
# ============================================================

def _handle_character(arguments):
    archetype = _get_text_argument(arguments, "archetype", "主角")
    genre = _get_text_argument(arguments, "genre", "玄幻")

    template = CHARACTER_ARCHETYPES.get(archetype)
    if not template:
        available = ", ".join(CHARACTER_ARCHETYPES.keys())
        return [TextContent(type="text", text=f"未找到'{archetype}'的角色模板。可用原型：{available}")]

    output = f"角色设定模板：{archetype}（{genre}类型）\n{'=' * 40}\n\n"
    output += "【核心特质】\n"
    for trait in template["core_traits"]:
        output += f"  • {trait}\n"
    output += "\n【常见背景设定】\n"
    for bg in template.get("common_backgrounds", []):
        output += f"  • {bg}\n"

    if "growth_patterns" in template:
        output += "\n【成长轨迹】\n"
        for pattern in template["growth_patterns"]:
            output += f"  • {pattern}\n"

    if "motivation_types" in template:
        output += "\n【动机类型】\n"
        for motivation in template["motivation_types"]:
            output += f"  • {motivation}\n"

    if "teaching_methods" in template:
        output += "\n【教导方式】\n"
        for method in template["teaching_methods"]:
            output += f"  • {method}\n"

    if "support_types" in template:
        output += "\n【支持类型】\n"
        for support in template["support_types"]:
            output += f"  • {support}\n"

    output += "\n【典型冲突】\n"
    for conflict in template.get("typical_conflicts", []):
        output += f"  • {conflict}\n"

    output += f"\n【{genre}类型特色建议】\n"
    genre_suggestions = {
        "玄幻": ["设计独特的修炼天赋", "安排关键的奇遇事件", "设定明确的复仇/守护动机"],
        "都市": ["设计隐藏的身份背景", "安排现实与能力的冲突", "设定接地气的成长目标"],
        "科幻": ["设计科技与人性的冲突", "安排技术突破的关键时刻", "设定宏大的宇宙观"],
        "悬疑": ["设计复杂的内心世界", "安排线索与真相的关联", "设定道德灰色地带"]
    }
    for suggestion in genre_suggestions.get(genre, ["根据世界观设计角色特色", "安排符合类型的情节冲突"]):
        output += f"  • {suggestion}\n"

    return [TextContent(type="text", text=output)]


# ============================================================
# generate_plot
# ============================================================

def _handle_plot(arguments):
    plot_type = _get_text_argument(arguments, "plot_type", "英雄之旅")
    genre = _get_text_argument(arguments, "genre", "玄幻")

    template = PLOT_TYPES.get(plot_type)
    if not template:
        for key in PLOT_TYPES:
            if plot_type in key or key in plot_type:
                template = PLOT_TYPES[key]
                plot_type = key
                break

    if not template:
        return [TextContent(type="text", text=f"未找到'{plot_type}'的情节模板。可用类型：{', '.join(PLOT_TYPES.keys())}")]

    output = f"情节设计模板：{plot_type}（{genre}类型）\n{'=' * 40}\n\n"
    output += f"【结构说明】{template['description']}\n\n"
    output += "【适用类型】\n"
    for suitable in template["suitable"]:
        output += f"  • {suitable}\n"
    output += "\n【情节阶段】\n"
    for i, stage in enumerate(template["stages"], 1):
        output += f"  {i}. {stage}\n"

    output += f"\n【{genre}类型应用建议】\n"
    genre_advice = {
        "玄幻": "在每个阶段融入修炼突破和战斗场景，注意力量展示的节奏",
        "都市": "注重现实感和代入感，在关键节点安排身份揭露或能力展示",
        "科幻": "利用科技设定制造独特的冲突和解决方案，注意逻辑严密性",
        "悬疑": "在每个阶段埋下线索和误导，控制信息释放的节奏"
    }
    output += f"  {genre_advice.get(genre, '根据具体类型调整各阶段的重点和节奏')}\n"

    return [TextContent(type="text", text=output)]


# ============================================================
# analyze_writing
# ============================================================

def _handle_analyze_writing(arguments):
    text = _get_text_argument(arguments, "text")
    if not text:
        return [TextContent(type="text", text="请提供要分析的文本或技法术语")]

    output = "写作技法分析\n" + "=" * 40 + "\n\n"

    found_terms = []
    for term, data in TECHNIQUE_TERMINOLOGY.items():
        if term in text or text in term:
            found_terms.append((term, data))

    if found_terms:
        output += "【相关术语解释】\n\n"
        for term, data in found_terms:
            output += f"📖 {term}（{data['level']}）\n"
            output += f"   定义：{data['definition']}\n"
            output += f"   用法：{data['usage']}\n"
            output += f"   相关：{', '.join(data['related'])}\n\n"

    text_lower = text.lower()
    related_methodologies = []
    for topic, data in WRITING_METHODOLOGY.items():
        topic_keywords = [topic]
        topic_keywords.extend(data.get("principles", []))
        for keyword in topic_keywords:
            if keyword in text_lower:
                related_methodologies.append(topic)
                break

    if related_methodologies:
        output += "【相关方法论】\n\n"
        for topic in related_methodologies[:2]:
            data = WRITING_METHODOLOGY[topic]
            output += f"📚 {topic}\n"
            output += f"   {data['description']}\n"
            output += "   核心原则：\n"
            for p in data["principles"][:3]:
                output += f"     • {p}\n"
            output += "\n"

    if not found_terms and not related_methodologies:
        output += f"未找到与'{text}'直接相关的术语或方法论。\n\n"
        output += "建议尝试以下关键词：\n"
        sample_terms = random.sample(list(TECHNIQUE_TERMINOLOGY.keys()), min(8, len(TECHNIQUE_TERMINOLOGY)))
        for term in sample_terms:
            output += f"  • {term}\n"

    return [TextContent(type="text", text=output)]


# ============================================================
# suggest_titles
# ============================================================

def _handle_suggest_titles(arguments):
    genre = _get_text_argument(arguments, "genre", "玄幻仙侠")
    theme = _get_text_argument(arguments, "theme")

    pattern_data = TITLE_PATTERNS.get(genre)
    if not pattern_data:
        for key in TITLE_PATTERNS:
            if genre in key or key in genre:
                pattern_data = TITLE_PATTERNS[key]
                genre = key
                break

    if not pattern_data:
        return [TextContent(type="text", text=f"未找到'{genre}'的标题模板。可用类型：{', '.join(TITLE_PATTERNS.keys())}")]

    output = f"标题推荐：{genre}类型\n"
    if theme:
        output += f"主题关键词：{theme}\n"
    output += "=" * 40 + "\n\n"

    output += f"【风格特点】{pattern_data['style']}\n\n"
    output += "【常用标题结构】\n"
    for pattern in pattern_data["patterns"]:
        output += f"  • {pattern}\n"
    output += "\n【热门词汇】\n"
    hot_words = pattern_data["hot_words"]
    output += f"  {', '.join(hot_words)}\n\n"

    output += "【标题生成建议】\n"
    if theme:
        theme_words = [w.strip() for w in re.split(r'[,，、\s]+', theme) if w.strip()]
        output += f"  基于主题'{theme}'的标题思路：\n"
        for word in theme_words[:3]:
            hot = random.choice(hot_words)
            output += f"    • {word}{hot}\n"
            output += f"    • {hot}之{word}\n"
    else:
        output += "  请提供主题关键词以生成具体标题建议\n"

    return [TextContent(type="text", text=output)]


# ============================================================
# generate_dialogue
# ============================================================

def _handle_dialogue(arguments):
    scenario = _get_text_argument(arguments, "scenario")
    if not scenario:
        return [TextContent(type="text", text=f"可用对话场景：{', '.join(DIALOGUE_TEMPLATES.keys())}")]

    template = DIALOGUE_TEMPLATES.get(scenario)
    if not template:
        for key in DIALOGUE_TEMPLATES:
            if scenario in key or key in scenario:
                template = DIALOGUE_TEMPLATES[key]
                scenario = key
                break

    if not template:
        available = ", ".join(DIALOGUE_TEMPLATES.keys())
        return [TextContent(type="text", text=f"未找到'{scenario}'的对话模板。可用场景：{available}")]

    output = f"对话模板：{scenario}\n" + "=" * 40 + "\n\n"
    output += f"【整体氛围】{template['tone']}\n\n"
    output += "【对话结构】\n"
    for i, stage in enumerate(template["structure"], 1):
        output += f"  {i}. {stage}\n"
    output += "\n【写作技巧】\n"
    for technique in template["techniques"]:
        output += f"  • {technique}\n"
    output += f"\n【示例】\n  \"{template['example']}\"\n\n"
    output += "【创作提示】\n"
    output += "  1. 对话要符合角色性格和身份\n"
    output += "  2. 善用潜台词，避免过于直白\n"
    output += "  3. 注意对话节奏，长短句交替\n"
    output += "  4. 通过动作和表情辅助对话表达\n"

    return [TextContent(type="text", text=output)]


# ============================================================
# 启动服务器
# ============================================================

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
