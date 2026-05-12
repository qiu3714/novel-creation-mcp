#!/usr/bin/env python3
"""
小说创作内容自动采集脚本 v3.0
==============================

功能：定期浏览各大平台的小说创作相关内容，提炼整合后更新到知识库中。

作者：自动化任务系统
版本：3.0.0
"""

import os
import sys
import json
import re
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from config import (
        PROJECT_ROOT, KNOWLEDGE_DIR, KNOWLEDGE_BASE_FILE, COLLECTED_CONTENT_FILE,
        PLATFORMS, COLLECTOR_CONFIG, LOGS_DIR, BACKUPS_DIR, REPORTS_DIR
    )
except ImportError:
    # 简化配置（当配置文件不可用时）
    PROJECT_ROOT = Path(__file__).parent.parent
    KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"
    KNOWLEDGE_BASE_FILE = KNOWLEDGE_DIR / "knowledge-base.json"
    COLLECTED_CONTENT_FILE = KNOWLEDGE_DIR / "collected_content.json"
    LOGS_DIR = PROJECT_ROOT / "logs"
    BACKUPS_DIR = PROJECT_ROOT / "backups"
    REPORTS_DIR = PROJECT_ROOT / "reports"

    # 平台配置（简化版）
    PLATFORMS = {
        "番茄小说": {
            "keywords": ["小说创作", "写作技巧", "网文教程"],
            "priority": 1,
            "enabled": True
        },
        "起点中文网": {
            "keywords": ["写作指导", "小说创作", "网文写作"],
            "priority": 1,
            "enabled": True
        },
        "B站": {
            "keywords": ["小说创作", "网文教程", "写作技巧"],
            "priority": 2,
            "enabled": True
        }
    }

    # 采集配置
    COLLECTOR_CONFIG = {
        "max_items_per_platform": 10,
        "relevance_threshold": 0,
        "deduplication_enabled": True,
        "report_enabled": True,
        "backup_before_update": True,
        "max_content_summary_length": 500,
        "max_key_points": 10
    }


class ContentType(Enum):
    """内容类型枚举"""
    TUTORIAL = "教程"
    GUIDE = "攻略"
    EXPERIENCE = "经验"
    CASE_STUDY = "案例"
    TEMPLATE = "模板"
    NEWS = "资讯"
    INTERVIEW = "访谈"
    OTHER = "其他"


@dataclass
class ContentItem:
    """内容条目数据结构"""
    id: str
    title: str
    platform: str
    content_type: ContentType
    content_summary: str
    key_points: List[str]
    keywords: List[str]
    relevance_score: float
    collected_at: str
    source_url: Optional[str] = None
    author: Optional[str] = None
    publish_date: Optional[str] = None
    tags: Optional[List[str]] = None
    status: str = "new"
    quality_score: float = 0.0
    application_scenario: Optional[str] = None
    practical_tips: Optional[List[str]] = None
    examples: Optional[List[str]] = None
    source_reference: Optional[str] = None
    first_collected: Optional[str] = None
    updated_at: Optional[str] = None


class ContentCollector:
    """内容采集器"""

    def __init__(self, kb_path: str = None, config: Dict = None):
        """
        初始化采集器
        
        Args:
            kb_path: 知识库文件路径
            config: 采集配置
        """
        self.kb_path = kb_path or str(KNOWLEDGE_BASE_FILE)
        self.collected_path = str(COLLECTED_CONTENT_FILE)
        self.config = config or COLLECTOR_CONFIG
        self.stats = {
            'total_collected': 0,
            'new_items': 0,
            'updated_items': 0,
            'failed_items': 0,
            'skipped_items': 0,
            'start_time': None,
            'end_time': None,
            'platform_stats': {}
        }
        
        # 设置日志
        self._setup_logging()
        
        # 延迟加载的知识库数据
        self._kb_data = None
        self._collected_data = None
        self._kb_loaded = False
        self._collected_loaded = False

    def _setup_logging(self):
        """设置日志系统"""
        log_dir = Path(LOGS_DIR)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"collector_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(str(log_file), encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _load_knowledge_base(self) -> dict:
        """延迟加载主知识库"""
        if self._kb_loaded:
            return self._kb_data
        
        try:
            if os.path.exists(self.kb_path):
                self.logger.info(f"正在加载主知识库: {self.kb_path}")
                file_size = os.path.getsize(self.kb_path)
                self.logger.info(f"主知识库文件大小: {file_size / 1024 / 1024:.2f} MB")
                
                with open(self.kb_path, 'r', encoding='utf-8') as f:
                    self._kb_data = json.load(f)
                
                # 确保必要字段存在
                if 'metadata' not in self._kb_data:
                    self._kb_data['metadata'] = {
                        'name': '小说创作知识库',
                        'version': '3.0.0',
                        'created_at': datetime.now().isoformat(),
                        'source': 'auto_content_collector'
                    }
                
                self._kb_loaded = True
                self.logger.info("主知识库加载成功")
                return self._kb_data
                
        except Exception as e:
            self.logger.error(f"加载主知识库失败: {e}")
        
        # 返回默认结构
        self._kb_data = {
            "metadata": {
                "name": "小说创作知识库",
                "version": "3.0.0",
                "description": "小说创作MCP工具的综合知识库",
                "created_at": datetime.now().isoformat(),
                "source": "auto_content_collector",
                "updated_at": datetime.now().isoformat()
            }
        }
        self._kb_loaded = True
        return self._kb_data

    def _load_collected_content(self) -> dict:
        """延迟加载采集内容"""
        if self._collected_loaded:
            return self._collected_data
        
        try:
            if os.path.exists(self.collected_path):
                self.logger.info(f"正在加载采集内容库: {self.collected_path}")
                
                with open(self.collected_path, 'r', encoding='utf-8') as f:
                    self._collected_data = json.load(f)
                
                # 确保必要字段存在
                if 'metadata' not in self._collected_data:
                    self._collected_data['metadata'] = {
                        'name': '采集内容库',
                        'version': '1.0.0',
                        'created_at': datetime.now().isoformat()
                    }
                if 'collected_content' not in self._collected_data:
                    self._collected_data['collected_content'] = []
                
                self._collected_loaded = True
                content_count = len(self._collected_data.get('collected_content', []))
                self.logger.info(f"采集内容库加载成功，共 {content_count} 条内容")
                return self._collected_data
                
        except Exception as e:
            self.logger.error(f"加载采集内容库失败: {e}")
        
        # 返回默认结构
        self._collected_data = {
            "metadata": {
                "name": "采集内容库",
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_items": 0
            },
            "collected_content": []
        }
        self._collected_loaded = True
        return self._collected_data

    def _save_knowledge_base(self):
        """保存主知识库"""
        try:
            os.makedirs(os.path.dirname(self.kb_path), exist_ok=True)
            
            # 创建备份
            if self.config.get('backup_before_update', True) and os.path.exists(self.kb_path):
                backup_dir = Path(BACKUPS_DIR)
                backup_dir.mkdir(parents=True, exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = backup_dir / f"knowledge_base_{timestamp}.json"
                
                with open(backup_path, 'w', encoding='utf-8') as f:
                    json.dump(self._kb_data, f, ensure_ascii=False, indent=2)
                
                self.logger.info(f"主知识库备份完成: {backup_path}")
            
            # 保存主知识库
            with open(self.kb_path, 'w', encoding='utf-8') as f:
                json.dump(self._kb_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"主知识库保存成功")
            
        except Exception as e:
            self.logger.error(f"保存主知识库失败: {e}")
            raise

    def _save_collected_content(self):
        """保存采集内容库"""
        try:
            os.makedirs(os.path.dirname(self.collected_path), exist_ok=True)
            
            # 更新统计信息
            self._collected_data['metadata']['last_updated'] = datetime.now().isoformat()
            self._collected_data['metadata']['total_items'] = len(self._collected_data.get('collected_content', []))
            
            # 保存
            with open(self.collected_path, 'w', encoding='utf-8') as f:
                json.dump(self._collected_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info("采集内容库保存成功")
            
        except Exception as e:
            self.logger.error(f"保存采集内容库失败: {e}")
            raise

    def _is_duplicate(self, title: str, content: str = "") -> bool:
        """检查是否重复"""
        if not self.config.get('deduplication_enabled', True):
            return False
        
        # 加载采集内容库
        collected_data = self._load_collected_content()
        existing_titles = [c.get('title', '').lower() for c in collected_data.get('collected_content', [])]
        
        title_lower = title.lower()
        
        # 完全匹配
        if title_lower in existing_titles:
            return True
        
        # 部分匹配（标题前20个字符相同）
        title_prefix = title_lower[:20]
        for existing in existing_titles:
            if existing.startswith(title_prefix) and len(title) > 20:
                return True
        
        return False

    def _generate_content_id(self, title: str, platform: str) -> str:
        """生成内容ID"""
        # 清理标题
        clean_title = re.sub(r'[^\w\u4e00-\u9fff]', '_', title)
        clean_title = clean_title[:30]
        
        # 平台缩写
        platform_abbr = ''.join([p[0] for p in platform if p.isalnum()])[:3]
        
        # 时间戳
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        
        return f"cc_{platform_abbr}_{timestamp}_{clean_title}"

    def _extract_key_points(self, content: str, title: str = "") -> List[str]:
        """提取内容要点"""
        key_points = []
        text = content + " " + title
        
        # 提取数字列表
        numbered_items = re.findall(r'(\d+)[.、:：]([^。！？\n]+)', text)
        for num, text in numbered_items:
            if len(text.strip()) > 3:
                key_points.append(f"{num}. {text.strip()}")
        
        # 提取关键词短语
        keyword_patterns = [
            r'([\u4e00-\u9fff]{2,8}(?:技巧|方法|原则|攻略|指南|秘诀|法则|公式|模板|要点|核心|关键|要素))',
            r'((?:如何|怎么|怎样)[^\s]{0,20})',
            r'([^\s]{0,15}(?:类型|模式|体系|结构|设计|构建|创作))'
        ]
        
        for pattern in keyword_patterns:
            matches = re.findall(pattern, text)
            key_points.extend([m.strip() for m in matches if len(m.strip()) > 3])
        
        # 去重并限制数量
        seen = set()
        unique_points = []
        for point in key_points:
            point_lower = point.lower()
            if point_lower not in seen and len(point) > 3:
                seen.add(point_lower)
                unique_points.append(point)
        
        max_points = self.config.get('max_key_points', 10)
        return unique_points[:max_points]

    def _calculate_relevance(self, title: str, content: str, platform_keywords: List[str]) -> float:
        """计算相关度得分"""
        if not platform_keywords:
            return 50.0
        
        text = (title + " " + content).lower()
        keywords_lower = [kw.lower() for kw in platform_keywords]
        
        # 计算关键词匹配数
        matched = sum(1 for kw in keywords_lower if kw in text)
        
        # 基础分数
        base_score = 30
        
        # 关键词匹配加分
        keyword_score = matched * 15
        
        # 标题包含关键词加分
        title_bonus = sum(10 for kw in keywords_lower if kw in title.lower())
        
        # 内容长度加分
        length_bonus = min(20, len(content) / 100)
        
        # 计算总分
        total_score = base_score + keyword_score + title_bonus + length_bonus
        
        return min(100, max(0, total_score))

    def _calculate_quality_score(self, content_item: ContentItem) -> float:
        """计算内容质量得分"""
        score = 50  # 基础分
        
        # 内容长度
        if len(content_item.content_summary) > 200:
            score += 10
        if len(content_item.content_summary) > 400:
            score += 5
        
        # 要点数量
        if len(content_item.key_points) >= 3:
            score += 10
        if len(content_item.key_points) >= 5:
            score += 5
        
        # 相关度
        if content_item.relevance_score >= 80:
            score += 15
        elif content_item.relevance_score >= 60:
            score += 10
        
        # 内容类型
        if content_item.content_type in [ContentType.TUTORIAL, ContentType.GUIDE]:
            score += 10
        
        return min(100, max(0, score))

    def _determine_content_type(self, content: str, title: str) -> ContentType:
        """判断内容类型"""
        text = content + " " + title
        
        type_keywords = {
            ContentType.TUTORIAL: ["教程", "教学", "入门", "基础", "学习"],
            ContentType.GUIDE: ["攻略", "指南", "手册", "大全", "宝典"],
            ContentType.EXPERIENCE: ["经验", "分享", "心得", "总结", "回顾"],
            ContentType.CASE_STUDY: ["案例", "分析", "解析", "研究", "解读"],
            ContentType.TEMPLATE: ["模板", "框架", "结构", "设计", "规划"],
            ContentType.NEWS: ["新闻", "资讯", "动态", "更新", "发布"],
            ContentType.INTERVIEW: ["访谈", "采访", "专访", "对话", "交流"]
        }
        
        for content_type, keywords in type_keywords.items():
            if any(kw in text for kw in keywords):
                return content_type
        
        return ContentType.OTHER

    def _fetch_from_platform(self, platform: str, config: Dict) -> List[Dict[str, str]]:
        """从平台获取内容（模拟）"""
        self.logger.info(f"正在采集 {platform} 的相关内容...")
        
        # 这里应该是真实的爬虫逻辑，目前使用模拟数据
        mock_results = {
            "番茄小说": [
                {
                    "title": "番茄小说写作全攻略：从构思到完本",
                    "content": "本文详细介绍番茄小说的写作技巧，包括如何设计吸引人的开头、如何保持节奏、如何设置爽点等核心内容。重点讲解三章定江山的法则，以及如何抓住读者的心。适合新手入门和进阶提升。",
                    "type": "教程"
                },
                {
                    "title": "网文写作必备：100个经典套路模板",
                    "content": "收集了网文写作中最常用的100个套路模板，涵盖逆袭、打脸、升级、装逼、系统流等经典情节模式。每个套路都有详细的使用说明和示例。",
                    "type": "素材"
                },
                {
                    "title": "如何设计让人印象深刻的反派角色",
                    "content": "反派角色是故事的重要组成部分，本文介绍了如何设计有魅力的反派角色。包括反派人设的十个类型、病娇型反派、疯批美人等多种设计思路。",
                    "type": "教程"
                },
                {
                    "title": "网文开篇黄金三章的写作秘诀",
                    "content": "揭秘网文开篇的写作技巧，如何在第一章就抓住读者。包括钩子设计、主角登场、冲突设置等核心要素。",
                    "type": "教程"
                },
                {
                    "title": "小说节奏掌控：让读者欲罢不能",
                    "content": "详细讲解小说节奏的掌控技巧，包括快节奏与慢节奏的切换、高潮与缓冲的处理、章节结尾的钩子设置等。",
                    "type": "教程"
                }
            ],
            "起点中文网": [
                {
                    "title": "起点白金大神访谈：如何打造爆款小说",
                    "content": "采访多位起点白金大神作家，分享他们的创作经验和成功秘诀。包含如何选择题材、如何设计大纲、如何保持日更等实战经验。",
                    "type": "访谈"
                },
                {
                    "title": "网络小说世界观构建完整指南",
                    "content": "从地理环境到社会结构，从力量体系到势力分布，全面解析如何构建一个完整的小说世界。包含多种类型小说的世界观设计模板。",
                    "type": "教程"
                },
                {
                    "title": "情节设计的黄金法则与经典结构",
                    "content": "介绍情节设计的核心原则，包括冲突设置、伏笔回收、节奏把控、三幕式结构、英雄之旅等经典叙事框架的运用。",
                    "type": "教程"
                },
                {
                    "title": "网络小说角色塑造的十大技巧",
                    "content": "深入讲解角色塑造的技巧，包括人物性格设计、人物弧光、角色关系、人物成长等方面。附赠多种角色模板。",
                    "type": "教程"
                },
                {
                    "title": "网文爽点设计：从压抑到爆发的艺术",
                    "content": "揭秘网文爽点的设计原理，包括爽点的类型、爽点的节奏、爽点的层次等方面。让你的小说让读者欲罢不能。",
                    "type": "教程"
                }
            ],
            "B站": [
                {
                    "title": "【写作教程】30分钟学会写网文开头",
                    "content": "视频教程，详细讲解网文开篇的写作技巧，包括如何设置钩子、如何快速进入剧情、如何展示主角特质等核心要素。适合新手入门。",
                    "type": "视频"
                },
                {
                    "title": "小说人物塑造技巧大揭秘",
                    "content": "从外貌到内心，从性格到行为，全面解析如何塑造立体的人物形象。包括人物设定卡模板、人物关系设计等实用内容。",
                    "type": "视频"
                },
                {
                    "title": "爽点设计的终极公式",
                    "content": "揭秘网文爽点的设计原理，包含九种经典爽点类型：奇遇、升级、寻宝、泡妞/恋爱、发财、欺人，助人、复仇、称霸。",
                    "type": "视频"
                },
                {
                    "title": "网文大纲写法详细教程",
                    "content": "手把手教你写网文大纲，包括主线设计、支线安排、章节规划等。让你告别卡文，写出结构清晰的小说。",
                    "type": "视频"
                },
                {
                    "title": "如何设计让人上头的角色",
                    "content": "讲解有魅力角色的设计方法，包括反差萌、病娇、傲娇等流行人设的塑造技巧。让你笔下的角色让读者又爱又恨。",
                    "type": "视频"
                }
            ],
            "抖音": [
                {
                    "title": "写作干货：三句话让读者爱上你的小说",
                    "content": "简洁实用的写作技巧，教你如何用三句话抓住读者的心。包括开篇钩子、冲突设置、悬念制造等核心技巧。",
                    "type": "短视频"
                },
                {
                    "title": "网文写作避坑指南大全",
                    "content": "总结网文写作中常见的误区和坑点，包括开篇毒点、人物崩塌、节奏失控等问题。帮助新手少走弯路。",
                    "type": "短视频"
                },
                {
                    "title": "如何制造故事悬念的技巧",
                    "content": "悬念是吸引读者的关键，本文介绍几种实用的悬念制造方法，包括信息差、伏笔设置、倒计时等技巧。",
                    "type": "短视频"
                },
                {
                    "title": "小说人物对话怎么写才吸引人",
                    "content": "教你如何写出有特色的角色对话，包括不同性格角色的说话方式、对话的功能性、潜台词的运用等。",
                    "type": "短视频"
                },
                {
                    "title": "网文日更三千的技巧分享",
                    "content": "分享网文日更的实用技巧，包括时间管理、大纲写作、快速构思等方法。让你轻松保持日更不断更。",
                    "type": "短视频"
                }
            ],
            "知乎": [
                {
                    "title": "写网络小说月入过万是种什么体验？",
                    "content": "多位全职网文作者分享他们的收入情况和创作经验。包括新人如何起步、签约注意事项、收入提升技巧等。",
                    "type": "问答"
                },
                {
                    "title": "如何评价当前网络小说的发展趋势？",
                    "content": "分析当前网文市场的发展趋势，包括热门题材分析、读者喜好变化，未来发展方向等。为创作者提供参考。",
                    "type": "问答"
                },
                {
                    "title": "网络小说的核心竞争力是什么？",
                    "content": "探讨网文创作的核心要素，包括故事性、人物塑造、文笔风格、更新速度等方面。帮助创作者找准方向。",
                    "type": "问答"
                },
                {
                    "title": "有哪些相见恨晚的网文写作技巧？",
                    "content": "分享多位老作者的经验技巧，包括大纲写法、卡文解决、人设设计等方面。都是实战总结的干货。",
                    "type": "问答"
                },
                {
                    "title": "网文新人如何选择适合自己的平台？",
                    "content": "对比分析各大网文平台的特点，包括番茄、起点、七猫等平台的优劣势。帮助新人选择最适合的平台。",
                    "type": "问答"
                }
            ],
            "微信公众号": [
                {
                    "title": "深度解析：网络小说的人物弧光设计",
                    "content": "详细讲解人物弧光的设计方法，包括主角的成长轨迹、内心转变、与其他角色的互动等。",
                    "type": "文章"
                },
                {
                    "title": "网文写作中的情绪张力营造技巧",
                    "content": "探讨如何在网文中营造情绪张力，包括情绪拉扯、情绪爆发、情绪递进等方面的技巧。",
                    "type": "文章"
                }
            ],
            "小红书": [
                {
                    "title": "超全的小说写作素材库分享",
                    "content": "分享多种写作素材，包括描写素材、情节素材、对话素材等。都是创作好帮手。",
                    "type": "笔记"
                },
                {
                    "title": "小说大纲模板直接套用",
                    "content": "分享多种小说大纲模板，适合不同类型的小说。直接套用，省时省力。",
                    "type": "笔记"
                }
            ]
        }
        
        return mock_results.get(platform, [])

    def collect_content(self, platforms: List[str] = None) -> List[ContentItem]:
        """执行内容采集"""
        self.stats['start_time'] = datetime.now()
        collected = []
        
        # 确定要采集的平台
        enabled_platforms = platforms or [p for p, config in PLATFORMS.items() if config.get('enabled', True)]
        
        self.logger.info(f"开始采集内容，启用的平台: {enabled_platforms}")
        self.logger.info("-" * 70)
        
        for platform in enabled_platforms:
            if platform not in PLATFORMS:
                self.logger.warning(f"未知平台: {platform}")
                continue
            
            platform_config = PLATFORMS[platform]
            platform_stats = {
                'total': 0,
                'new': 0,
                'skipped': 0,
                'failed': 0
            }
            
            try:
                results = self._fetch_from_platform(platform, platform_config)
                max_items = self.config.get('max_items_per_platform', 10)
                
                for result in results[:max_items]:
                    platform_stats['total'] += 1
                    
                    # 检查重复
                    if self._is_duplicate(result["title"], result["content"]):
                        self.logger.debug(f"跳过重复内容: {result['title']}")
                        platform_stats['skipped'] += 1
                        self.stats['skipped_items'] += 1
                        continue
                    
                    # 提取关键信息
                    key_points = self._extract_key_points(result["content"], result["title"])
                    relevance = self._calculate_relevance(
                        result["title"],
                        result["content"],
                        platform_config["keywords"]
                    )
                    
                    # 检查相关度阈值
                    threshold = self.config.get('relevance_threshold', 0)
                    if threshold > 0 and relevance < threshold:
                        self.logger.debug(f"跳过低相关度内容: {result['title']} (相关度: {relevance}%)")
                        platform_stats['skipped'] += 1
                        self.stats['skipped_items'] += 1
                        continue
                    
                    # 判断内容类型
                    content_type = self._determine_content_type(result["content"], result["title"])
                    
                    # 创建内容项
                    content_item = ContentItem(
                        id=self._generate_content_id(result["title"], platform),
                        title=result["title"],
                        platform=platform,
                        content_type=content_type,
                        content_summary=result["content"][:self.config.get('max_content_summary_length', 500)],
                        key_points=key_points,
                        keywords=platform_config["keywords"],
                        relevance_score=relevance,
                        collected_at=datetime.now().isoformat(),
                        status="new"
                    )
                    
                    # 计算质量得分
                    content_item.quality_score = self._calculate_quality_score(content_item)
                    
                    collected.append(content_item)
                    platform_stats['new'] += 1
                    self.stats['new_items'] += 1
                    
                    self.logger.info(f"✓ 采集到: {result['title']} (相关度: {relevance}%, 质量: {content_item.quality_score:.1f}%)")
                
            except Exception as e:
                self.logger.error(f"采集 {platform} 内容时出错: {e}")
                platform_stats['failed'] += 1
                self.stats['failed_items'] += 1
                continue
            
            # 记录平台统计
            self.stats['platform_stats'][platform] = platform_stats
            self.logger.info(f"平台 {platform} 采集完成: 新增 {platform_stats['new']}, 跳过 {platform_stats['skipped']}")
        
        self.stats['total_collected'] = len(collected)
        self.stats['end_time'] = datetime.now()
        
        self.logger.info("-" * 70)
        self.logger.info(f"采集完成，共采集到 {len(collected)} 条内容")
        
        return collected

    def update_knowledge_base(self, collected_content: List[ContentItem]):
        """更新知识库"""
        self.logger.info("开始更新知识库...")
        
        # 确保采集内容库已加载
        collected_data = self._load_collected_content()
        
        for item in collected_content:
            # 转换为字典
            item_dict = asdict(item)
            item_dict['content_type'] = item.content_type.value
            
            # 检查是否已存在
            existing = [c for c in collected_data.get('collected_content', []) 
                       if c["title"] == item.title]
            
            if existing:
                # 更新现有内容
                idx = collected_data["collected_content"].index(existing[0])
                item_dict["status"] = "updated"
                item_dict["previous_update"] = existing[0].get("collected_at")
                item_dict["updated_at"] = datetime.now().isoformat()
                collected_data["collected_content"][idx] = item_dict
                self.logger.info(f"更新已有内容: {item.title}")
                self.stats['updated_items'] += 1
            else:
                # 添加新内容
                item_dict["status"] = "new"
                item_dict["first_collected"] = datetime.now().isoformat()
                collected_data["collected_content"].append(item_dict)
                self.logger.info(f"新增内容: {item.title}")
        
        # 保存采集内容库
        self._save_collected_content()
        
        # 更新主知识库的元数据
        kb_data = self._load_knowledge_base()
        kb_data['metadata']['updated_at'] = datetime.now().isoformat()
        kb_data['metadata']['total_items'] = len(collected_data.get('collected_content', []))
        kb_data['metadata']['last_collection_stats'] = {
            "collected": self.stats['total_collected'],
            "new": self.stats['new_items'],
            "updated": self.stats['updated_items'],
            "skipped": self.stats['skipped_items'],
            "failed": self.stats['failed_items'],
            "duration_seconds": (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        }
        
        # 保存主知识库
        self._save_knowledge_base()

    def generate_report(self) -> str:
        """生成采集报告"""
        collected_data = self._load_collected_content()
        content = collected_data.get("collected_content", [])
        
        # 平台统计
        platform_counts = {}
        for item in content:
            platform = item["platform"]
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        # 计算执行时间
        duration = ""
        if self.stats['start_time'] and self.stats['end_time']:
            duration = f"{(self.stats['end_time'] - self.stats['start_time']).total_seconds():.2f}秒"
        
        # 生成报告
        report = f"""# 📚 内容采集报告

## 基本信息

| 项目 | 数值 |
|------|------|
| 📅 采集时间 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
| 📊 本次采集 | {self.stats['total_collected']} 条 |
| ✨ 新增内容 | {self.stats['new_items']} 条 |
| 🔄 更新内容 | {self.stats['updated_items']} 条 |
| ⏭️ 跳过内容 | {self.stats['skipped_items']} 条 |
| ❌ 失败次数 | {self.stats['failed_items']} 次 |
| ⏱️ 执行耗时 | {duration} |
| 📦 采集库总计 | {len(content)} 条 |

## 📈 采集统计

| 平台 | 数量 | 占比 |
|------|------|------|
"""
        
        total = len(content)
        for platform, count in sorted(platform_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            report += f"| {platform} | {count} 条 | {percentage:.1f}% |\n"
        
        report += "\n## 📝 本次采集内容\n\n"
        
        if content:
            # 按采集时间排序，显示最近的内容
            recent_content = sorted(content, key=lambda x: x.get('collected_at', ''), reverse=True)[:10]
            
            for i, item in enumerate(recent_content, 1):
                report += f"### {i}. {item['title']}\n\n"
                report += f"- **来源平台**: {item['platform']}\n"
                report += f"- **内容类型**: {item['content_type']}\n"
                report += f"- **相关度评分**: {item['relevance_score']:.1f}%\n"
                report += f"- **质量评分**: {item.get('quality_score', 0):.1f}%\n"
                
                if item.get('key_points'):
                    points = item['key_points'][:3]
                    report += f"- **核心要点**: {', '.join(points)}...\n"
                
                report += f"- **采集时间**: {item.get('collected_at', '未知')}\n\n"
        else:
            report += "\n暂无采集内容。\n"
        
        report += f"""
## ⚙️ 系统信息

- **采集器版本**: 3.0.0
- **知识库版本**: {collected_data.get('metadata', {}).get('version', '1.0.0')}
- **最后更新**: {collected_data.get('metadata', {}).get('last_updated', '未知')}

---
*本报告由小说创作内容自动采集系统生成*
"""
        
        return report

    def save_report(self, report: str):
        """保存报告"""
        try:
            report_dir = Path(REPORTS_DIR)
            report_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = report_dir / f"采集报告_{timestamp}.md"
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            self.logger.info(f"报告已保存到: {report_path}")
            
        except Exception as e:
            self.logger.error(f"保存报告失败: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return self.stats.copy()

    def run(self, save_report: bool = True) -> Dict[str, Any]:
        """执行完整的采集流程"""
        try:
            self.logger.info("=" * 70)
            self.logger.info("🎯 小说创作内容自动采集系统 v3.0")
            self.logger.info("=" * 70)
            
            # 执行采集
            collected = self.collect_content()
            
            # 更新知识库
            if collected:
                self.update_knowledge_base(collected)
            
            # 生成报告
            if save_report and self.config.get('report_enabled', True):
                report = self.generate_report()
                self.save_report(report)
            
            # 返回结果
            return {
                "success": True,
                "stats": self.get_stats(),
                "collected_count": len(collected)
            }
            
        except Exception as e:
            self.logger.error(f"采集任务执行失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "stats": self.get_stats()
            }


def main():
    """主函数"""
    try:
        # 创建采集器
        collector = ContentCollector()
        
        # 执行采集
        result = collector.run(save_report=True)
        
        # 输出结果
        print("\n" + "=" * 70)
        if result["success"]:
            print("✅ 采集任务完成！")
            print(f"   • 新增内容: {result['stats']['new_items']} 条")
            print(f"   • 更新内容: {result['stats']['updated_items']} 条")
            print(f"   • 跳过内容: {result['stats']['skipped_items']} 条")
            print(f"   • 失败次数: {result['stats']['failed_items']} 次")
            
            if result['stats']['start_time'] and result['stats']['end_time']:
                duration = (result['stats']['end_time'] - result['stats']['start_time']).total_seconds()
                print(f"   • 执行耗时: {duration:.2f}秒")
        else:
            print(f"❌ 采集任务失败: {result['error']}")
        
        print("=" * 70)
        
        return 0 if result["success"] else 1
        
    except Exception as e:
        print(f"❌ 程序执行错误: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
