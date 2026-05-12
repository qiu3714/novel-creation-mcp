"""
知识库智能提示词系统 v2.0
==========================
功能：为知识库内容录入提供专业的提示词，确保高质量知识记录
使用统一的 config.py 配置
"""

import sys
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import KNOWLEDGE_SECTIONS


@dataclass
class PromptSection:
    section_id: str
    name: str
    description: str
    quality_standards: List[str]
    required_fields: List[str]
    example_format: str
    anti_patterns: List[str]


class KnowledgeBasePrompts:

    _sections: Dict[str, PromptSection] = None

    @classmethod
    def _init_sections(cls):
        if cls._sections is not None:
            return

        cls._sections = {}

        section_extra = {
            "character_design": {
                "quality_standards": [
                    "必须包含角色的核心矛盾和内在冲突",
                    "需要提供具体的性格表现方法，而非抽象描述",
                    "角色成长弧线必须有清晰的起点和终点",
                    "必须考虑角色与世界观的契合度"
                ],
                "required_fields": ["核心特质", "成长轨迹", "关键冲突", "设计技巧"],
                "example_format": "【角色类型】+【核心矛盾】+【成长方向】+【设计要点】",
                "anti_patterns": [
                    "避免过于完美的角色设定（玛丽苏/杰克苏）",
                    "避免性格标签化（如：冷酷=不说话）",
                    "避免成长缺乏铺垫（突然变强）",
                    "避免动机不合理（为坏而坏）"
                ]
            },
            "plot_structure": {
                "quality_standards": [
                    "必须包含完整的冲突-升级-解决链条",
                    "需要提供具体的节奏控制方法",
                    "伏笔设计必须有明确的回收计划",
                    "必须考虑读者的情绪曲线"
                ],
                "required_fields": ["结构框架", "冲突设计", "节奏控制", "伏笔技巧"],
                "example_format": "【结构类型】+【冲突层级】+【节奏要点】+【经典案例】",
                "anti_patterns": [
                    "避免冲突过于单一（只有打斗）",
                    "避免节奏失控（高潮过密或过疏）",
                    "避免伏笔忘记回收",
                    "避免逻辑漏洞（时间线矛盾等）"
                ]
            },
            "worldbuilding": {
                "quality_standards": [
                    "必须包含力量体系的等级和代价机制",
                    "需要提供世界观的内在逻辑",
                    "地理/历史设定需与故事主线相关",
                    "必须考虑设定的可扩展性"
                ],
                "required_fields": ["核心设定", "力量体系", "运行逻辑", "设计要点"],
                "example_format": "【世界类型】+【力量体系】+【核心规则】+【扩展方向】",
                "anti_patterns": [
                    "避免设定堆砌（为了复杂而复杂）",
                    "避免力量体系崩坏（后期数值失控）",
                    "避免设定前后矛盾",
                    "避免世界观与角色脱节"
                ]
            },
            "writing_techniques": {
                "quality_standards": [
                    "必须包含具体的写作技巧和方法",
                    "需要提供正反对比的示例",
                    "技巧必须具有可操作性",
                    "必须说明适用场景和限制条件"
                ],
                "required_fields": ["技巧名称", "使用方法", "适用场景", "示例对比"],
                "example_format": "【技法名称】+【操作步骤】+【适用场景】+【正反示例】",
                "anti_patterns": [
                    "避免过于抽象的描述（如：要写得生动）",
                    "避免脱离实际的理论（无法落地）",
                    "避免技巧堆砌（缺乏重点）",
                    "避免示例过于简单（缺乏说服力）"
                ]
            },
            "dialogue_generation": {
                "quality_standards": [
                    "必须体现角色的独特性格",
                    "需要包含潜台词和言外之意",
                    "对话必须推动情节发展",
                    "必须符合场景氛围"
                ],
                "required_fields": ["对话类型", "角色特点", "场景设定", "写作技巧"],
                "example_format": "【对话场景】+【角色性格】+【潜台词设计】+【示例对话】",
                "anti_patterns": [
                    "避免所有角色说话方式相同",
                    "避免对话过于直白（缺乏潜台词）",
                    "避免对话不推动剧情（水对话）",
                    "避免对话节奏拖沓"
                ]
            },
            "mythology": {
                "quality_standards": [
                    "必须准确引用神话原文或出处",
                    "需要提供现代创作的改编思路",
                    "素材必须具有故事性和戏剧性",
                    "必须说明文化背景和象征意义"
                ],
                "required_fields": ["神话体系", "核心故事", "象征意义", "创作改编"],
                "example_format": "【神话来源】+【核心故事】+【象征意义】+【改编方向】",
                "anti_patterns": [
                    "避免张冠李戴（混淆不同体系）",
                    "避免过度简化（失去原味）",
                    "避免文化不敏感（冒犯性改编）",
                    "避免素材与创作需求脱节"
                ]
            },
            "templates": {
                "quality_standards": [
                    "必须包含完整的模板框架",
                    "需要提供具体的使用方法和步骤",
                    "模板必须经过验证（有成功案例）",
                    "必须说明适用范围和限制"
                ],
                "required_fields": ["模板名称", "框架结构", "使用步骤", "成功案例"],
                "example_format": "【模板名称】+【框架结构】+【使用方法】+【案例验证】",
                "anti_patterns": [
                    "避免模板过于僵化（缺乏灵活性）",
                    "避免模板过于复杂（难以使用）",
                    "避免模板缺乏验证（纸上谈兵）",
                    "避免模板与实际创作脱节"
                ]
            },
            "genresearch": {
                "quality_standards": [
                    "必须包含该类型的核心特征",
                    "需要提供读者画像和市场分析",
                    "必须包含代表作品分析",
                    "必须说明创作要点和常见误区"
                ],
                "required_fields": ["类型特征", "读者画像", "代表作品", "创作要点"],
                "example_format": "【类型名称】+【核心特征】+【读者需求】+【创作指南】",
                "anti_patterns": [
                    "避免类型定义过于宽泛",
                    "避免忽略读者需求",
                    "避免脱离市场实际",
                    "避免创作建议过于笼统"
                ]
            },
            "platform_guides": {
                "quality_standards": [
                    "必须包含平台的最新规则",
                    "需要提供签约和推荐机制",
                    "必须包含成功作者的经验",
                    "必须说明平台特色和读者偏好"
                ],
                "required_fields": ["平台概况", "签约规则", "推荐机制", "创作建议"],
                "example_format": "【平台名称】+【核心规则】+【推荐机制】+【运营建议】",
                "anti_patterns": [
                    "避免信息过时（规则已变更）",
                    "避免忽略平台特色",
                    "避免建议过于笼统",
                    "避免忽略竞争环境"
                ]
            },
            "monetization": {
                "quality_standards": [
                    "必须包含具体的变现渠道",
                    "需要提供收入预期和案例",
                    "必须包含版权保护知识",
                    "必须说明不同阶段的变现策略"
                ],
                "required_fields": ["变现渠道", "收入预期", "成功案例", "注意事项"],
                "example_format": "【变现方式】+【收入预期】+【成功案例】+【风险提示】",
                "anti_patterns": [
                    "避免夸大收入预期",
                    "避免忽略版权风险",
                    "避免建议过于理想化",
                    "避免忽略长期规划"
                ]
            }
        }

        for section_id, section_config in KNOWLEDGE_SECTIONS.items():
            extra = section_extra.get(section_id, {})
            cls._sections[section_id] = PromptSection(
                section_id=section_id,
                name=section_config["name"],
                description=section_config["description"],
                quality_standards=extra.get("quality_standards", ["内容需准确、实用"]),
                required_fields=extra.get("required_fields", ["核心内容", "应用场景"]),
                example_format=extra.get("example_format", "【主题】+【核心要点】+【应用方法】"),
                anti_patterns=extra.get("anti_patterns", ["避免内容空洞", "避免脱离实际"])
            )

    @classmethod
    def get_section(cls, section_id: str) -> PromptSection:
        cls._init_sections()
        return cls._sections.get(section_id)

    @classmethod
    def get_all_sections(cls) -> Dict[str, PromptSection]:
        cls._init_sections()
        return cls._sections

    @classmethod
    def generate_collection_prompt(cls, section_id: str, raw_content: str = "") -> str:
        section = cls.get_section(section_id)
        if not section:
            return f"未知分区: {section_id}"

        prompt = f"""你是一个专业的小说创作知识库管理员。请根据以下标准整理和优化知识内容。

## 目标分区
- 分区名称: {section.name}
- 分区描述: {section.description}

## 质量标准
"""
        for i, standard in enumerate(section.quality_standards, 1):
            prompt += f"{i}. {standard}\n"

        prompt += "\n## 必需字段\n"
        for field in section.required_fields:
            prompt += f"- {field}\n"

        prompt += f"\n## 输出格式\n请按照以下格式输出：\n{section.example_format}\n"

        prompt += "\n## 避免的问题\n"
        for pattern in section.anti_patterns:
            prompt += f"- {pattern}\n"

        if raw_content:
            prompt += f"\n## 原始内容\n{raw_content}\n"

        prompt += """
## 处理要求
1. 提取核心知识点，去除冗余信息
2. 确保内容准确、实用、可操作
3. 添加具体案例或示例
4. 标注内容来源（如有）
5. 评估内容质量（1-10分）
"""
        return prompt

    @classmethod
    def generate_classification_prompt(cls, content: str) -> str:
        sections_desc = "\n".join(
            f"- {s.section_id}: {s.name} - {s.description}"
            for s in cls.get_all_sections().values()
        )

        return f"""请对以下内容进行分类，判断它应该归入哪个知识库分区。

## 可选分区
{sections_desc}

## 分类规则
1. 根据内容主题和关键词判断主要分区
2. 如果内容涉及多个分区，选择最相关的作为主分区
3. 评估内容与分区的相关性（1-10分）
4. 评估内容质量（优秀/良好/一般/需改进）

## 待分类内容
{content}

## 输出格式
- 主分区: [分区ID]
- 次分区: [分区ID]（如有）
- 相关性评分: [1-10]
- 质量评估: [优秀/良好/一般/需改进]
- 分类理由: [简要说明]
"""

    @classmethod
    def generate_quality_check_prompt(cls, section_id: str, content: str) -> str:
        section = cls.get_section(section_id)
        if not section:
            return f"未知分区: {section_id}"

        criteria_desc = "\n".join(
            f"- {c['name']}（权重{int(c['weight']*100)}%）: {c['description']}"
            for c in cls._get_quality_criteria()
        )
        section_reqs = "\n".join(f"- {s}" for s in section.quality_standards)

        return f"""请对以下内容进行质量评估。

## 评估分区: {section.name}

## 评估标准
{criteria_desc}

## 分区特定要求
{section_reqs}

## 待评估内容
{content}

## 输出格式
- 总分: [1-10]
- 完整性: [1-10] - [评价]
- 准确性: [1-10] - [评价]
- 相关性: [1-10] - [评价]
- 清晰度: [1-10] - [评价]
- 实用性: [1-10] - [评价]
- 改进建议: [具体建议]
"""

    @classmethod
    def _get_quality_criteria(cls) -> List[Dict]:
        return [
            {"name": "完整性", "weight": 0.2, "description": "内容是否完整，是否缺少关键信息"},
            {"name": "准确性", "weight": 0.25, "description": "信息是否准确，是否有错误"},
            {"name": "相关性", "weight": 0.2, "description": "与分区主题的相关程度"},
            {"name": "清晰度", "weight": 0.15, "description": "表达是否清晰易懂"},
            {"name": "实用性", "weight": 0.2, "description": "内容是否具有实际应用价值"}
        ]

    @classmethod
    def generate_summary_prompt(cls, content: str, max_length: int = 200) -> str:
        return f"""请对以下内容生成简洁的摘要。

## 要求
1. 摘要长度不超过{max_length}字
2. 保留核心信息和关键观点
3. 使用简洁明了的语言
4. 突出实用价值

## 原始内容
{content}

## 输出格式
- 核心摘要: [摘要内容]
- 关键词: [关键词1, 关键词2, ...]
- 实用价值: [简要说明]
"""

    @classmethod
    def generate_batch_import_prompt(cls, contents: List[Dict[str, str]]) -> str:
        prompt = """请批量处理以下内容，为每条内容提供分类和质量评估。

## 处理要求
1. 为每条内容判断最适合的分区
2. 评估内容质量（1-10分）
3. 提取核心知识点
4. 判断是否值得录入（质量>=4分）

## 待处理内容
"""
        for i, item in enumerate(contents, 1):
            prompt += f"\n### 内容 {i}\n"
            prompt += f"标题: {item.get('title', '无标题')}\n"
            prompt += f"内容: {item.get('content', '')[:500]}\n"

        prompt += """
## 输出格式（每条内容）
- 序号: [编号]
- 推荐分区: [分区ID]
- 质量评分: [1-10]
- 核心要点: [要点1, 要点2, ...]
- 是否录入: [是/否]
- 原因: [简要说明]
"""
        return prompt

    @classmethod
    def generate_update_prompt(cls, section_id: str, existing_content: str, new_content: str) -> str:
        section = cls.get_section(section_id)
        if not section:
            return f"未知分区: {section_id}"

        return f"""请评估以下新内容是否应该更新到{section.name}分区。

## 现有内容
{existing_content[:500]}

## 新内容
{new_content[:500]}

## 评估要求
1. 新内容是否提供了新的知识点？
2. 新内容是否与现有内容重复？
3. 新内容的质量是否达到录入标准？
4. 如果需要更新，应该如何整合？

## 输出格式
- 是否更新: [是/否]
- 更新类型: [新增/替换/补充]
- 整合建议: [具体建议]
- 质量对比: [新内容 vs 现有内容]
"""
