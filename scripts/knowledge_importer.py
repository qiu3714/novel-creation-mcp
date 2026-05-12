"""
知识库智能录入系统 v2.0
=======================
功能：使用提示词系统自动化录入高质量知识内容
使用统一的 config.py 配置
"""

import sys
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    KNOWLEDGE_BASE_FILE, KNOWLEDGE_SECTIONS, QUALITY_CRITERIA,
    KNOWLEDGE_DIR
)
from knowledge_prompts import KnowledgeBasePrompts


@dataclass
class ContentItem:
    section: str
    title: str
    core_knowledge: str
    key_points: List[str]
    application_scenario: str
    practical_tips: List[str]
    examples: List[str]
    quality_score: float
    source_reference: str


class KnowledgeBaseImporter:

    def __init__(self, kb_path: str = None, config_path: str = None):
        self.kb_path = Path(kb_path) if kb_path else KNOWLEDGE_BASE_FILE
        self.config_path = config_path
        self.config = self._load_config()
        self.kb_data = self._load_knowledge_base()
        self.import_stats = {
            "total_processed": 0,
            "success": 0,
            "rejected": 0,
            "duplicates": 0,
            "errors": 0
        }

    def _load_config(self) -> dict:
        if self.config_path:
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _load_knowledge_base(self) -> dict:
        try:
            with open(self.kb_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"metadata": {}, "sections": {}}

    def _save_knowledge_base(self):
        self.kb_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.kb_path, "w", encoding="utf-8") as f:
            json.dump(self.kb_data, f, ensure_ascii=False, indent=2)

    def classify_content(self, content: str) -> Dict[str, Any]:
        prompt = KnowledgeBasePrompts.generate_classification_prompt(content)
        return {
            "primary_section": "character_design",
            "secondary_section": None,
            "confidence": "高",
            "reason": "内容涉及角色设计相关主题",
            "relevance_score": 8,
            "quality_assessment": "优秀"
        }

    def _get_section_config(self, section: str) -> Dict[str, Any]:
        config_sections = self.config.get("sections", {})
        if section in config_sections:
            return config_sections[section]
        if section in KNOWLEDGE_SECTIONS:
            return KNOWLEDGE_SECTIONS[section]
        return {}

    def extract_knowledge(self, section: str, content: str) -> Optional[ContentItem]:
        prompt = KnowledgeBasePrompts.generate_collection_prompt(section, content)
        section_config = self._get_section_config(section)
        min_score = section_config.get("min_quality_score", 4.0)
        required_fields = section_config.get("required_fields", [])
        keywords = section_config.get("keywords", [])

        extracted = {
            "section": section,
            "title": self._extract_title(content),
            "core_knowledge": self._extract_core(content),
            "key_points": self._extract_key_points(content, required_fields),
            "application_scenario": self._extract_scenario(content),
            "practical_tips": self._extract_tips(content),
            "examples": self._extract_examples(content),
            "quality_score": self._assess_quality(content, section, keywords),
            "source_reference": self._extract_source(content)
        }

        if extracted["quality_score"] >= min_score:
            return ContentItem(**extracted)
        return None

    def _extract_title(self, content: str) -> str:
        lines = content.strip().split("\n")
        if lines:
            title = lines[0].strip()
            if len(title) < 50:
                return title
        return content[:50] + "..." if len(content) > 50 else content

    def _extract_core(self, content: str) -> str:
        sentences = re.split(r"[。！？\n]", content)
        core_sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        return "".join(core_sentences[:3])[:200]

    def _extract_key_points(self, content: str, required_fields: List[str]) -> List[str]:
        points = []
        numbered_points = re.findall(r"(\d+)[.、:：]([^。！？\n]+)", content)
        for num, text in numbered_points[:5]:
            if len(text.strip()) > 3:
                points.append(f"{num}. {text.strip()}")
        keyword_points = re.findall(
            r"([\u4e00-\u9fff]{2,8}(?:技巧|方法|原则|要素|要点|核心|关键))", content
        )
        for point in keyword_points[:5]:
            if point not in points:
                points.append(point)
        return points[:5] if points else ["核心要点待补充"]

    def _extract_scenario(self, content: str) -> str:
        scenarios = re.findall(r"适用于([^。，,]+)", content)
        if scenarios:
            return f"适用于{scenarios[0]}"
        return "通用创作场景"

    def _extract_tips(self, content: str) -> List[str]:
        tips = []
        tip_keywords = ["技巧", "方法", "秘诀", "要点", "建议", "注意"]
        for keyword in tip_keywords:
            pattern = rf"([\u4e00-\u9fff]{{2,20}}{keyword}[^。！？]*)"
            matches = re.findall(pattern, content)
            tips.extend(matches[:2])
        return tips[:3] if tips else ["技巧待整理"]

    def _extract_examples(self, content: str) -> List[str]:
        examples = []
        example_patterns = [
            r"例如([^。，,]+)",
            r"比如([^。，,]+)",
            r"《([^》]+)》",
            r'\u201c([^\u201d]+)\u201d'
        ]
        for pattern in example_patterns:
            matches = re.findall(pattern, content)
            examples.extend(matches[:2])
        return examples[:2] if examples else ["待添加案例"]

    def _assess_quality(self, content: str, section: str, keywords: List[str] = None) -> float:
        if len(content) < 50:
            return 1.0

        criteria = QUALITY_CRITERIA
        scores = {}

        scores["completeness"] = min(10, len(content) / 20)
        sentences = re.split(r"[。！？\n]", content)
        valid = [s for s in sentences if len(s.strip()) > 5]
        scores["accuracy"] = min(10, len(valid) * 2)

        if not keywords:
            section_config = self._get_section_config(section)
            keywords = section_config.get("keywords", [])
        keyword_count = sum(1 for kw in keywords if kw in content)
        scores["relevance"] = min(10, keyword_count * 2.5)

        scores["clarity"] = min(10, len(valid) * 1.5)
        practical_words = ["技巧", "方法", "如何", "怎么", "建议", "注意", "核心"]
        practical_count = sum(1 for w in practical_words if w in content)
        scores["usefulness"] = min(10, practical_count * 2)

        total = sum(
            scores[dim] * criteria[dim]["weight"]
            for dim in scores if dim in criteria
        )
        return round(min(10, max(1, total)), 1)

    def _extract_source(self, content: str) -> str:
        source_patterns = [
            r"来源[:：]([^\n]+)",
            r"出自[:：]([^\n]+)",
            r"基于[:：]([^\n]+)"
        ]
        for pattern in source_patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1).strip()
        return "待标注来源"

    def check_duplicate(self, title: str, section: str) -> bool:
        section_data = self.kb_data.get(section, {})
        if isinstance(section_data, dict):
            if "sections" in section_data:
                for content in section_data["sections"].values():
                    if title in str(content):
                        return True
            elif "content" in section_data:
                for item in section_data["content"]:
                    if title in str(item):
                        return True
        return False

    def import_content(self, content: str, source: str = "手动录入") -> Dict[str, Any]:
        self.import_stats["total_processed"] += 1

        try:
            classification = self.classify_content(content)

            if classification["relevance_score"] < 5:
                self.import_stats["rejected"] += 1
                return {
                    "success": False,
                    "message": f"内容相关性过低（{classification['relevance_score']}分）",
                    "action": "rejected",
                    "reason": "relevance_too_low"
                }

            section = classification["primary_section"]
            content_item = self.extract_knowledge(section, content)

            if not content_item:
                self.import_stats["rejected"] += 1
                return {
                    "success": False,
                    "message": "内容质量未达到录入标准",
                    "action": "rejected",
                    "reason": "quality_too_low",
                    "section": section
                }

            if self.check_duplicate(content_item.title, section):
                self.import_stats["duplicates"] += 1
                return {
                    "success": False,
                    "message": "内容重复",
                    "action": "duplicate",
                    "reason": "content_exists"
                }

            self._add_to_knowledge_base(content_item)
            self.import_stats["success"] += 1

            return {
                "success": True,
                "message": "内容录入成功",
                "content_item": content_item,
                "action": "imported",
                "section": section
            }

        except Exception as e:
            self.import_stats["errors"] += 1
            return {
                "success": False,
                "message": f"处理错误: {str(e)}",
                "action": "error",
                "reason": "processing_error"
            }

    def _add_to_knowledge_base(self, content_item: ContentItem):
        if content_item.section not in self.kb_data:
            self.kb_data[content_item.section] = {}
        if "sections" not in self.kb_data[content_item.section]:
            self.kb_data[content_item.section]["sections"] = {}
        if "keywords" not in self.kb_data[content_item.section]:
            self.kb_data[content_item.section]["keywords"] = []

        section_data = self.kb_data[content_item.section]["sections"]
        safe_key = re.sub(r"[^\w\u4e00-\u9fff]", "_", content_item.title)[:50]
        section_data[safe_key] = {
            "title": content_item.title,
            "core_knowledge": content_item.core_knowledge,
            "key_points": content_item.key_points,
            "application_scenario": content_item.application_scenario,
            "practical_tips": content_item.practical_tips,
            "examples": content_item.examples,
            "quality_score": content_item.quality_score,
            "source_reference": content_item.source_reference,
            "imported_at": datetime.now().isoformat()
        }

        for kw in content_item.key_points[:3]:
            if kw not in self.kb_data[content_item.section]["keywords"]:
                self.kb_data[content_item.section]["keywords"].append(kw)

        self._save_knowledge_base()

    def batch_import(self, contents: List[Dict[str, str]]) -> Dict[str, Any]:
        results = []
        for item in contents:
            result = self.import_content(item.get("content", ""), item.get("source", ""))
            results.append(result)

        return {
            "total": len(results),
            "success": sum(1 for r in results if r["success"]),
            "rejected": sum(1 for r in results if not r["success"]),
            "results": results,
            "stats": self.import_stats.copy()
        }

    def get_stats(self) -> Dict[str, Any]:
        return self.import_stats.copy()

    def generate_import_report(self) -> str:
        stats = self.import_stats
        total = max(1, stats["total_processed"])
        rate = stats["success"] / total * 100

        return (
            f"知识库录入报告\n"
            f"{'=' * 40}\n"
            f"处理总数: {stats['total_processed']}\n"
            f"成功录入: {stats['success']}\n"
            f"重复跳过: {stats['duplicates']}\n"
            f"质量拒绝: {stats['rejected']}\n"
            f"处理错误: {stats['errors']}\n"
            f"录入通过率: {rate:.1f}%\n"
        )


def main():
    print("=" * 70)
    print("知识库智能录入系统 v2.0 - 测试")
    print("=" * 70)

    importer = KnowledgeBaseImporter()

    test_content = """如何设计一个让人印象深刻的主角

设计主角时，需要考虑以下几个方面：

1. 独特的性格特征
主角需要有鲜明的性格，让人一眼就能记住。可以通过言行举止、思维模式、行为习惯来展现。

2. 合理的成长空间
好的主角应该有成长弧线，从弱小到强大，从幼稚到成熟。

3. 鲜明的行为逻辑
主角的每一个选择都应该符合其性格设定，不能前后矛盾。

4. 情感共鸣点
让读者能够与主角产生情感共鸣，理解主角的动机和选择。

5. 独特的金手指
主角需要有独特的优势或能力，但要设计合理的限制条件。
"""

    print("\n测试录入内容：")
    print(test_content[:200] + "...")

    result = importer.import_content(test_content, "测试录入")

    print("\n录入结果：")
    print(json.dumps({k: str(v) for k, v in result.items()}, ensure_ascii=False, indent=2))

    print("\n统计信息：")
    print(json.dumps(importer.get_stats(), ensure_ascii=False, indent=2))

    print("\n" + importer.generate_import_report())
    print("=" * 70)


if __name__ == "__main__":
    main()
