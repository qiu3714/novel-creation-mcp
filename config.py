"""
小说创作MCP工具 - 项目配置
===========================

统一的项目配置文件，包含所有模块共享的配置参数
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 知识库相关路径
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"
KNOWLEDGE_BASE_FILE = KNOWLEDGE_DIR / "knowledge-base.json"
COLLECTED_CONTENT_FILE = KNOWLEDGE_DIR / "collected_content.json"
KNOWLEDGE_PROMPTS_CONFIG = KNOWLEDGE_DIR / "knowledge_prompts_config.json"
AUTOMATION_PROMPTS_CONFIG = KNOWLEDGE_DIR / "automation_prompts_config.json"

# 脚本目录
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
TASK_CONFIG_FILE = SCRIPTS_DIR / "task_config.json"
COLLECTOR_CONFIG_FILE = SCRIPTS_DIR / "collector_config.json"

# 日志和备份
LOGS_DIR = PROJECT_ROOT / "logs"
BACKUPS_DIR = PROJECT_ROOT / "backups"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Python解释器路径（可在此处自定义，留空则使用系统默认Python）
PYTHON_EXECUTABLE = ""

# 采集平台配置
PLATFORMS = {
    "番茄小说": {
        "url": "https://www.tomatofiction.com",
        "keywords": ["小说创作", "写作技巧", "网文教程", "小说大纲", "人物设定", "开篇写法", "爽点设计"],
        "content_types": ["文案", "教程", "经验分享"],
        "priority": 1,
        "enabled": True
    },
    "起点中文网": {
        "url": "https://www.qidian.com",
        "keywords": ["写作指导", "小说创作", "网文写作", "情节设计", "世界观", "大纲构思", "角色塑造"],
        "content_types": ["教程", "专栏", "访谈"],
        "priority": 1,
        "enabled": True
    },
    "B站": {
        "url": "https://www.bilibili.com",
        "keywords": ["小说创作", "网文教程", "写作技巧", "故事构思", "角色设计", "写作干货", "写作素材"],
        "content_types": ["视频", "教程", "经验"],
        "priority": 2,
        "enabled": True
    },
    "抖音": {
        "url": "https://www.douyin.com",
        "keywords": ["小说创作", "写作干货", "网文技巧", "故事灵感", "写作素材", "网文写作", "写作技巧"],
        "content_types": ["短视频", "文案", "教程"],
        "priority": 2,
        "enabled": True
    },
    "知乎": {
        "url": "https://www.zhihu.com",
        "keywords": ["小说创作", "网文写作", "写作经验", "情节构思", "人物塑造", "小说写作", "创作技巧"],
        "content_types": ["问答", "专栏", "经验"],
        "priority": 2,
        "enabled": True
    },
    "微信公众号": {
        "url": "https://mp.weixin.qq.com",
        "keywords": ["小说创作", "写作技巧", "网文教程", "故事创作", "写作干货"],
        "content_types": ["文章", "教程", "经验"],
        "priority": 3,
        "enabled": True
    },
    "小红书": {
        "url": "https://www.xiaohongshu.com",
        "keywords": ["小说创作", "写作技巧", "网文", "故事灵感", "写作素材"],
        "content_types": ["笔记", "教程"],
        "priority": 3,
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

# 调度配置
SCHEDULER_CONFIG = {
    "name": "小说创作内容自动采集",
    "description": "定时采集各大平台小说创作相关内容并更新知识库",
    "version": "2.0.0",
    "schedule": {
        "type": "weekly",
        "day": "周一",
        "hour": 9,
        "minute": 0
    },
    "enabled": True,
    "settings": {
        "auto_backup": True,
        "max_history": 50,
        "notification_enabled": False,
        "retry_on_failure": True,
        "max_retries": 3
    }
}

# MCP服务器配置
MCP_SERVER_CONFIG = {
    "name": "novel-creation-mcp",
    "version": "3.0.0-rc.1",
    "description": "小说创作MCP工具",
    "tools": [
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
        "generate_dialogue"
    ]
}

# 知识库分区配置
KNOWLEDGE_SECTIONS = {
    "character_design": {
        "name": "角色设计",
        "description": "人物塑造、角色弧线、性格设定、配角设计等",
        "keywords": ["角色", "人物", "主角", "配角", "反派", "性格", "人设", "人物塑造", "角色设计", "角色弧线", "人物弧线", "角色成长"],
        "priority": 1,
        "min_quality_score": 4.0,
        "max_items_per_import": 20,
        "content_types": ["方法论", "案例", "模板", "素材"]
    },
    "plot_structure": {
        "name": "情节结构",
        "description": "故事结构、情节设计、冲突构建、悬念设置等",
        "keywords": ["情节", "剧情", "故事线", "冲突", "悬念", "伏笔", "高潮", "反转", "节奏", "叙事", "大纲"],
        "priority": 1,
        "min_quality_score": 4.0,
        "max_items_per_import": 20,
        "content_types": ["方法论", "案例", "模板", "素材"]
    },
    "worldbuilding": {
        "name": "世界观构建",
        "description": "世界设定、力量体系、种族设定、地理环境等",
        "keywords": ["世界观", "设定", "魔法体系", "力量体系", "修炼体系", "种族", "地理", "历史", "文明", "势力"],
        "priority": 1,
        "min_quality_score": 3.5,
        "max_items_per_import": 15,
        "content_types": ["方法论", "案例", "模板", "素材"]
    },
    "writing_techniques": {
        "name": "写作技法",
        "description": "写作技巧、文笔提升、描写方法、叙事手法等",
        "keywords": ["写作", "技巧", "文笔", "描写", "叙事技巧", "写作技法", "写作方法", "修辞", "文风", "视角"],
        "priority": 2,
        "min_quality_score": 4.0,
        "max_items_per_import": 20,
        "content_types": ["方法论", "案例", "模板", "素材"]
    },
    "dialogue_generation": {
        "name": "对话生成",
        "description": "对话写作、台词设计、语言风格等",
        "keywords": ["对话", "台词", "语言", "口癖", "对白", "对话写作", "对话技巧"],
        "priority": 2,
        "min_quality_score": 3.5,
        "max_items_per_import": 10,
        "content_types": ["方法论", "案例", "模板", "素材"]
    },
    "mythology": {
        "name": "神话传说",
        "description": "神话体系、传说典故、文化原型等",
        "keywords": ["神话", "传说", "典故", "原型", "神话体系", "民间传说"],
        "priority": 3,
        "min_quality_score": 3.0,
        "max_items_per_import": 10,
        "content_types": ["素材", "案例"]
    },
    "templates": {
        "name": "写作模板",
        "description": "万能模板、写作公式、爆款套路等",
        "keywords": ["模板", "公式", "套路", "框架", "万能模板", "爽点", "爆点", "金手指"],
        "priority": 1,
        "min_quality_score": 4.0,
        "max_items_per_import": 15,
        "content_types": ["模板", "公式"]
    },
    "genresearch": {
        "name": "类型研究",
        "description": "不同网文类型的特点和创作方法",
        "keywords": ["玄幻", "仙侠", "都市", "科幻", "悬疑", "言情", "历史", "重生", "穿越", "系统"],
        "priority": 2,
        "min_quality_score": 3.5,
        "max_items_per_import": 15,
        "content_types": ["分析", "案例", "方法论"]
    },
    "platform_guides": {
        "name": "平台指南",
        "description": "各网文平台的规则、特点和运营指南",
        "keywords": ["平台", "签约", "投稿", "编辑", "推荐", "榜单", "番茄", "起点"],
        "priority": 2,
        "min_quality_score": 3.0,
        "max_items_per_import": 10,
        "content_types": ["指南", "规则", "经验"]
    },
    "monetization": {
        "name": "盈利变现",
        "description": "写作变现、版权运营、收入提升等",
        "keywords": ["盈利", "赚钱", "收入", "变现", "稿费", "收益", "版权", "IP"],
        "priority": 3,
        "min_quality_score": 3.0,
        "max_items_per_import": 10,
        "content_types": ["指南", "案例", "方法论"]
    }
}

# 内容类型枚举
CONTENT_TYPES = ["方法论", "案例", "模板", "素材", "指南", "规则", "经验", "分析", "公式"]

# 质量评分标准
QUALITY_CRITERIA = {
    "completeness": {"weight": 0.2, "description": "内容完整性"},
    "accuracy": {"weight": 0.25, "description": "信息准确性"},
    "relevance": {"weight": 0.2, "description": "主题相关性"},
    "clarity": {"weight": 0.15, "description": "表达清晰度"},
    "usefulness": {"weight": 0.2, "description": "实用价值"}
}

# 日志配置
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": str(LOGS_DIR / "app.log"),
            "formatter": "standard",
            "level": "DEBUG",
            "encoding": "utf-8"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True
        }
    }
}


def ensure_directories():
    """确保所有必要的目录存在"""
    dirs = [
        KNOWLEDGE_DIR,
        SCRIPTS_DIR,
        LOGS_DIR,
        BACKUPS_DIR,
        REPORTS_DIR
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def get_config(section: str) -> dict:
    """获取配置信息"""
    configs = {
        "platforms": PLATFORMS,
        "collector": COLLECTOR_CONFIG,
        "scheduler": SCHEDULER_CONFIG,
        "mcp_server": MCP_SERVER_CONFIG,
        "logging": LOGGING_CONFIG
    }
    return configs.get(section, {})


def get_path(path_name: str) -> Path:
    """获取路径"""
    paths = {
        "project_root": PROJECT_ROOT,
        "knowledge_dir": KNOWLEDGE_DIR,
        "knowledge_base": KNOWLEDGE_BASE_FILE,
        "collected_content": COLLECTED_CONTENT_FILE,
        "knowledge_prompts_config": KNOWLEDGE_PROMPTS_CONFIG,
        "automation_prompts_config": AUTOMATION_PROMPTS_CONFIG,
        "scripts_dir": SCRIPTS_DIR,
        "task_config": TASK_CONFIG_FILE,
        "collector_config": COLLECTOR_CONFIG_FILE,
        "logs_dir": LOGS_DIR,
        "backups_dir": BACKUPS_DIR,
        "reports_dir": REPORTS_DIR,
        "python": Path(PYTHON_EXECUTABLE)
    }
    return paths.get(path_name)


# 初始化时确保目录存在
ensure_directories()
