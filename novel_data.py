"""
小说创作MCP工具 - 静态数据模块
===============================

从server.py提取的所有静态数据，包括：
- 情节类型定义
- 内容分类映射
- 写作方法论
- 技法术语库
- 世界观模板
- 角色生成模板
- 对话生成模板
- 标题生成模板
"""

# ============================================================
# 情节类型定义
# ============================================================

PLOT_TYPES = {
    "英雄之旅": {
        "description": "经典的英雄旅程叙事结构",
        "stages": ["平凡世界", "冒险召唤", "拒绝召唤", "遇见导师", "跨越门槛", "考验/盟友/敌人", "接近洞穴", "磨难", "奖赏", "归途", "复活", "带着万能药归来"],
        "suitable": ["奇幻", "冒险", "成长"]
    },
    "三幕结构": {
        "description": "最经典的叙事结构",
        "stages": ["建置（介绍人物和世界）", "对抗（冲突升级）", "解决（高潮和结局）"],
        "suitable": ["通用"]
    },
    "起承转合": {
        "description": "中国传统叙事结构",
        "stages": ["起（开端）", "承（发展）", "转（转折）", "合（结局）"],
        "suitable": ["东方玄幻", "武侠"]
    },
    "多线并行": {
        "description": "多条故事线同时推进",
        "stages": ["主线确立", "支线展开", "线索交织", "汇聚高潮"],
        "suitable": ["群像", "权谋", "史诗"]
    },
    "倒叙揭秘": {
        "description": "从结果开始，逐步揭示真相",
        "stages": ["结果呈现", "线索铺设", "真相渐显", "最终揭秘"],
        "suitable": ["悬疑", "推理", "心理"]
    }
}

# ============================================================
# 内容分类映射
# ============================================================

CLASSIFICATION_MAPPING = {
    "角色": "character_design",
    "人物": "character_design",
    "主角": "character_design",
    "配角": "character_design",
    "反派": "character_design",
    "性格": "character_design",
    "人物塑造": "character_design",
    "人物设定": "character_design",
    "角色塑造": "character_design",
    "角色设计": "character_design",
    "角色弧线": "character_design",
    "人物弧线": "character_design",
    "角色成长": "character_design",
    "角色设定": "character_design",
    "情节": "plot_structure",
    "剧情": "plot_structure",
    "故事线": "plot_structure",
    "冲突": "plot_structure",
    "悬念": "plot_structure",
    "伏笔": "plot_structure",
    "高潮": "plot_structure",
    "反转": "plot_structure",
    "节奏": "plot_structure",
    "叙事": "plot_structure",
    "大纲": "plot_structure",
    "故事结构": "plot_structure",
    "情节设计": "plot_structure",
    "剧情设计": "plot_structure",
    "世界观": "worldbuilding",
    "设定": "worldbuilding",
    "魔法体系": "worldbuilding",
    "力量体系": "worldbuilding",
    "修炼体系": "worldbuilding",
    "功法体系": "worldbuilding",
    "战力体系": "worldbuilding",
    "种族": "worldbuilding",
    "地理": "worldbuilding",
    "历史": "worldbuilding",
    "文明": "worldbuilding",
    "势力": "worldbuilding",
    "宗门": "worldbuilding",
    "功法": "worldbuilding",
    "境界": "worldbuilding",
    "战力": "worldbuilding",
    "写作": "writing_techniques",
    "技巧": "writing_techniques",
    "文笔": "writing_techniques",
    "描写": "writing_techniques",
    "叙事技巧": "writing_techniques",
    "写作技法": "writing_techniques",
    "写作方法": "writing_techniques",
    "写作手法": "writing_techniques",
    "修辞": "writing_techniques",
    "文风": "writing_techniques",
    "视角": "writing_techniques",
    "开篇": "writing_techniques",
    "结尾": "writing_techniques",
    "过渡": "writing_techniques",
    "对话": "dialogue_generation",
    "台词": "dialogue_generation",
    "语言": "dialogue_generation",
    "口癖": "dialogue_generation",
    "对白": "dialogue_generation",
    "对话写作": "dialogue_generation",
    "对话技巧": "dialogue_generation",
    "对话设计": "dialogue_generation",
    "神话": "mythology",
    "传说": "mythology",
    "典故": "mythology",
    "原型": "mythology",
    "神话体系": "mythology",
    "民间传说": "mythology",
    "神话原型": "mythology",
    "神话设定": "mythology",
    "模板": "templates",
    "公式": "templates",
    "套路": "templates",
    "框架": "templates",
    "万能模板": "templates",
    "写作模板": "templates",
    "创作模板": "templates",
    "模板套路": "templates",
    "爽点": "templates",
    "爆点": "templates",
    "金手指": "templates",
    "逆袭": "templates",
    "打脸": "templates",
    "装逼": "templates",
    "虐主": "templates",
    "无敌": "templates",
    "玄幻": "genresearch",
    "仙侠": "genresearch",
    "都市": "genresearch",
    "科幻": "genresearch",
    "悬疑": "genresearch",
    "言情": "genresearch",
    "历史": "genresearch",
    "军事": "genresearch",
    "游戏": "genresearch",
    "体育": "genresearch",
    "灵异": "genresearch",
    "同人": "genresearch",
    "系统": "genresearch",
    "重生": "genresearch",
    "穿越": "genresearch",
    "无限": "genresearch",
    "末日": "genresearch",
    "修仙": "genresearch",
    "异世": "genresearch",
    "平台": "platform_guides",
    "签约": "platform_guides",
    "投稿": "platform_guides",
    "编辑": "platform_guides",
    "推荐": "platform_guides",
    "榜单": "platform_guides",
    "平台规则": "platform_guides",
    "平台指南": "platform_guides",
    "网文平台": "platform_guides",
    "番茄": "platform_guides",
    "起点": "platform_guides",
    "七猫": "platform_guides",
    "书旗": "platform_guides",
    "飞卢": "platform_guides",
    "塔读": "platform_guides",
    "刺猬猫": "platform_guides",
    "盈利": "monetization",
    "赚钱": "monetization",
    "收入": "monetization",
    "变现": "monetization",
    "稿费": "monetization",
    "收益": "monetization",
    "版权": "monetization",
    "IP": "monetization",
    "IP改编": "monetization",
    "网文收入": "monetization",
    "写作赚钱": "monetization",
    "靠写作赚钱": "monetization"
}

# ============================================================
# 写作方法论数据库
# ============================================================

WRITING_METHODOLOGY = {
    "角色塑造": {
        "description": "系统化的角色创建方法论",
        "principles": ["角色需要内在矛盾", "性格需要多维度展现", "成长弧线需要清晰", "动机需要合理可信"],
        "methods": [
            "冰山理论：只展现10%的性格，让读者自行想象其余90%",
            "对比法：通过与其他角色的对比突出特质",
            "细节刻画：通过小动作、习惯、口癖展现性格",
            "压力测试：在极端情况下展现真实性格"
        ],
        "common_mistakes": ["性格过于单一", "动机不够充分", "成长过于突兀", "配角过于脸谱化"],
        "examples": ["《斗破苍穹》萧炎的成长弧线", "《诡秘之主》克莱恩的多重身份"]
    },
    "情节设计": {
        "description": "情节构建的核心方法",
        "principles": ["冲突是故事的引擎", "悬念要层层递进", "伏笔要前后呼应", "节奏要张弛有度"],
        "methods": [
            "雪花写作法：从一句话概括逐步扩展",
            "冲突升级法：从个人到社会到宇宙级冲突",
            "反转设计：在读者最意想不到的地方反转",
            "多线交织：多条故事线汇聚产生化学反应"
        ],
        "common_mistakes": ["冲突过于单一", "伏笔忘记回收", "节奏失控", "逻辑漏洞"],
        "examples": ["《庆余年》的权谋设计", "《诡秘之主》的伏笔网络"]
    },
    "世界观构建": {
        "description": "世界观设定的系统方法",
        "principles": ["设定要有内在逻辑", "力量体系要有代价", "历史要与现实呼应", "细节要经得起推敲"],
        "methods": [
            "冰山法则：展现10%，隐藏90%",
            "内在逻辑：所有设定要有统一的底层逻辑",
            "力量代价：力量越大，代价越大",
            "历史厚度：通过历史增加世界真实感"
        ],
        "common_mistakes": ["设定前后矛盾", "力量体系崩坏", "世界过于空洞", "设定堆砌过多"],
        "examples": ["《诡秘之主》的序列体系", "《凡人修仙传》的修炼体系"]
    },
    "对话写作": {
        "description": "对话创作的核心技巧",
        "principles": ["对话要展现性格", "潜台词比明示更重要", "对话要推动剧情", "节奏要符合场景"],
        "methods": [
            "角色语言指纹：每个角色有独特的说话方式",
            "潜台词设计：字面意思与真实意图的差距",
            "冲突对话：通过对话展现冲突和张力",
            "信息控制：通过对话控制信息释放节奏"
        ],
        "common_mistakes": ["所有角色说话方式相同", "对话过于直白", "对话不推动剧情", "对话节奏拖沓"],
        "examples": ["金庸小说中的对话艺术", "《庆余年》中的权谋对话"]
    },
    "开篇设计": {
        "description": "小说开篇的创作方法",
        "principles": ["前三章决定生死", "快速建立代入感", "尽早展示核心卖点", "制造足够的悬念"],
        "methods": [
            "冲突开场：直接进入冲突场景",
            "悬念开场：抛出核心悬念吸引读者",
            "反差开场：用强烈反差吸引注意力",
            "金手指展示：尽早展示核心设定"
        ],
        "common_mistakes": ["开篇过于平淡", "设定介绍过多", "节奏过于缓慢", "没有核心卖点"],
        "examples": ["《斗破苍穹》的退婚开局", "《全职高手》的退役开局"]
    },
    "爽点设计": {
        "description": "网文爽点的设计方法",
        "principles": ["压抑后的释放更爽", "超出预期更爽", "打脸要彻底", "装逼要自然"],
        "methods": [
            "先抑后扬：先压抑主角，再强力反弹",
            "实力碾压：用绝对实力碾压对手",
            "身份揭露：关键时刻揭露真实身份",
            "连环打脸：连续打脸多个反派"
        ],
        "common_mistakes": ["爽点间隔太长", "打脸不够彻底", "装逼过于刻意", "压抑时间过长"],
        "examples": ["《斗破苍穹》的三年之约", "《全职高手》的重返巅峰"]
    }
}

# ============================================================
# 技法术语库
# ============================================================

TECHNIQUE_TERMINOLOGY = {
    "小白文": {
        "definition": "通俗易懂、节奏明快的网文类型",
        "usage": "指语言简单直白、情节爽快的小说",
        "related": ["爽文", "快餐文"],
        "level": "基础"
    },
    "爽文": {
        "definition": "以让读者感到爽快为主要目标的小说",
        "usage": "情节设计以读者爽感为核心",
        "related": ["小白文", "打脸文"],
        "level": "基础"
    },
    "金手指": {
        "definition": "主角获得的特殊能力或优势",
        "usage": "为主角提供超越常人的起点或成长速度",
        "related": ["外挂", "系统", "奇遇"],
        "level": "基础"
    },
    "打脸": {
        "definition": "主角用实力证明自己，让看不起自己的人颜面扫地",
        "usage": "网文中最常见的爽点之一",
        "related": ["装逼", "逆袭", "爽点"],
        "level": "基础"
    },
    "装逼": {
        "definition": "主角展示实力或身份时的夸张表现",
        "usage": "需要自然不刻意，否则会显得尴尬",
        "related": ["打脸", "扮猪吃虎"],
        "level": "基础"
    },
    "扮猪吃虎": {
        "definition": "隐藏实力，在关键时刻才展现真实能力",
        "usage": "制造反差感和爽感的经典套路",
        "related": ["装逼", "打脸", "实力碾压"],
        "level": "中级"
    },
    "节奏": {
        "definition": "故事推进的速度和张弛有度",
        "usage": "好的节奏能让读者欲罢不能",
        "related": ["爽点间隔", "情节密度"],
        "level": "进阶"
    },
    "伏笔": {
        "definition": "提前埋下的线索，在后文揭示",
        "usage": "增加故事的深度和回味感",
        "related": ["草蛇灰线", "前后呼应"],
        "level": "进阶"
    },
    "草蛇灰线": {
        "definition": "隐晦的伏笔手法，如蛇行草中、灰画线条",
        "usage": "高级伏笔技巧，需要精心设计",
        "related": ["伏笔", "暗线"],
        "level": "高级"
    },
    "角色弧线": {
        "definition": "角色在故事中的成长和变化轨迹",
        "usage": "好的角色弧线能让角色更加立体",
        "related": ["角色成长", "性格发展"],
        "level": "进阶"
    },
    "代入感": {
        "definition": "读者对主角的认同和情感投入程度",
        "usage": "代入感是网文成功的关键因素",
        "related": ["共鸣", "沉浸感"],
        "level": "基础"
    },
    "沉浸感": {
        "definition": "读者沉浸在故事世界中的感觉",
        "usage": "通过细节描写和节奏控制营造",
        "related": ["代入感", "氛围营造"],
        "level": "进阶"
    },
    "套路": {
        "definition": "经过验证的有效叙事模式",
        "usage": "套路是前人经验的总结，合理使用能提高成功率",
        "related": ["模板", "公式"],
        "level": "基础"
    },
    "反套路": {
        "definition": "故意打破读者预期的写法",
        "usage": "在套路泛滥时使用能带来新鲜感",
        "related": ["反转", "创新"],
        "level": "进阶"
    },
    "人设": {
        "definition": "角色的设定和形象",
        "usage": "好的人设能让读者记住角色",
        "related": ["角色塑造", "性格设定"],
        "level": "基础"
    },
    "崩人设": {
        "definition": "角色行为与之前设定不符",
        "usage": "写作中需要避免的问题",
        "related": ["人设", "角色一致性"],
        "level": "基础"
    },
    "毒点": {
        "definition": "让读者弃书的负面情节",
        "usage": "需要尽量避免的写作雷区",
        "related": ["劝退", "弃书"],
        "level": "基础"
    },
    "断章": {
        "definition": "在关键时刻结束章节，制造悬念",
        "usage": "网文常用的技巧，能增加追读率",
        "related": ["悬念", "钩子"],
        "level": "中级"
    },
    "水文": {
        "definition": "无意义的填充文字，拖慢节奏",
        "usage": "需要避免的写作问题",
        "related": ["注水", "拖沓"],
        "level": "基础"
    },
    "大纲": {
        "definition": "故事的整体规划和结构设计",
        "usage": "写作前的准备工作，决定故事走向",
        "related": ["细纲", "故事线"],
        "level": "基础"
    },
    "细纲": {
        "definition": "详细的章节规划",
        "usage": "比大纲更详细的写作规划",
        "related": ["大纲", "章节规划"],
        "level": "中级"
    },
    "主线": {
        "definition": "故事的核心情节线",
        "usage": "所有支线都应服务于主线",
        "related": ["支线", "故事线"],
        "level": "基础"
    },
    "支线": {
        "definition": "辅助主线的次要情节线",
        "usage": "丰富故事内容，增加可读性",
        "related": ["主线", "副本"],
        "level": "中级"
    },
    "副本": {
        "definition": "独立于主线的小型故事单元",
        "usage": "网文中常见的结构，类似游戏中的副本",
        "related": ["支线", "单元剧"],
        "level": "中级"
    },
    "升级": {
        "definition": "主角实力的提升",
        "usage": "网文中最核心的爽点之一",
        "related": ["突破", "进阶", "升级流"],
        "level": "基础"
    },
    "突破": {
        "definition": "跨越境界或实力的飞跃",
        "usage": "修炼体系中的关键节点",
        "related": ["升级", "境界"],
        "level": "基础"
    },
    "装逼打脸": {
        "definition": "装逼和打脸的组合套路",
        "usage": "网文中最经典的爽点模式",
        "related": ["装逼", "打脸", "爽点"],
        "level": "基础"
    },
    "先抑后扬": {
        "definition": "先压抑后释放的叙事手法",
        "usage": "让爽点更加爽快的经典技法",
        "related": ["压抑", "释放", "爽点"],
        "level": "中级"
    },
    "草蛇灰线伏延千里": {
        "definition": "长线伏笔的高级写法",
        "usage": "需要极高的规划能力",
        "related": ["伏笔", "草蛇灰线"],
        "level": "高级"
    }
}

# ============================================================
# 世界观模板
# ============================================================

WORLD_TEMPLATES = {
    "修仙世界": {
        "core_elements": ["境界体系", "功法分类", "灵根设定", "宗门势力", "天材地宝"],
        "power_system": "灵气修炼",
        "typical_settings": ["宗门", "秘境", "仙界", "凡界"],
        "conflict_sources": ["境界突破", "资源争夺", "宗门争斗", "天劫"]
    },
    "玄幻世界": {
        "core_elements": ["力量等级", "种族设定", "大陆地理", "远古秘辛", "神器系统"],
        "power_system": "多元力量体系",
        "typical_settings": ["帝国", "学院", "战场", "异域"],
        "conflict_sources": ["种族战争", "大陆争霸", "远古阴谋", "天才对决"]
    },
    "都市世界": {
        "core_elements": ["社会背景", "势力分布", "隐藏势力", "特殊能力", "现代科技"],
        "power_system": "异能/古武/科技",
        "typical_settings": ["都市", "家族", "组织", "暗世界"],
        "conflict_sources": ["势力争斗", "商业竞争", "隐藏身份", "都市传说"]
    },
    "末日世界": {
        "core_elements": ["灾难类型", "生存资源", "变异生物", "人类聚落", "科技残留"],
        "power_system": "异能/改造/科技",
        "typical_settings": ["废墟", "避难所", "荒野", "危险区"],
        "conflict_sources": ["资源争夺", "怪物威胁", "人性考验", "文明重建"]
    },
    "游戏世界": {
        "core_elements": ["等级系统", "职业体系", "装备系统", "任务系统", "公会势力"],
        "power_system": "游戏化成长",
        "typical_settings": ["新手村", "主城", "副本", "竞技场"],
        "conflict_sources": ["公会战争", "Boss挑战", "排名竞争", "游戏阴谋"]
    }
}

# ============================================================
# 角色生成模板数据
# ============================================================

CHARACTER_ARCHETYPES = {
    "主角": {
        "core_traits": ["坚韧不拔", "成长潜力", "正义感"],
        "common_backgrounds": ["废材逆袭", "重生复仇", "天才陨落", "意外获得能力"],
        "growth_patterns": ["实力提升", "心智成熟", "责任觉醒", "情感成长"],
        "typical_conflicts": ["能力不足", "信任危机", "道德困境", "身份认同"]
    },
    "反派": {
        "core_traits": ["强大", "有魅力", "有信念"],
        "common_backgrounds": ["天才堕落", "理想破灭", "被迫选择", "天赋异禀"],
        "motivation_types": ["权力欲望", "复仇执念", "理念冲突", "生存本能"],
        "typical_conflicts": ["与主角理念冲突", "内部矛盾", "手下背叛", "自我怀疑"]
    },
    "导师": {
        "core_traits": ["智慧", "经验", "神秘"],
        "common_backgrounds": ["隐世高手", "退役强者", "神秘组织", "远古存在"],
        "teaching_methods": ["实战训练", "生死考验", "谜语指引", "放手让弟子闯"],
        "typical_conflicts": ["过去的秘密", "保护与放手", "理念传承", "命运安排"]
    },
    "配角": {
        "core_traits": ["忠诚", "互补", "有特色"],
        "common_backgrounds": ["青梅竹马", "不打不相识", "同病相怜", "使命相随"],
        "support_types": ["战斗辅助", "情报支持", "情感支撑", "后勤保障"],
        "typical_conflicts": ["实力差距", "理念分歧", "情感纠葛", "身份差异"]
    }
}

# ============================================================
# 对话生成模板数据
# ============================================================

DIALOGUE_TEMPLATES = {
    "冲突对话": {
        "structure": ["挑衅/质疑", "反驳/回应", "升级", "爆发/转折"],
        "tone": "紧张、对抗",
        "techniques": ["潜台词", "双关", "反问", "沉默"],
        "example": "你以为你赢了？（停顿）这才刚刚开始。"
    },
    "情感对话": {
        "structure": ["铺垫", "试探", "表白/交心", "回应"],
        "tone": "温柔、真挚",
        "techniques": ["欲言又止", "细节描写", "环境烘托", "动作暗示"],
        "example": "我从未想过要改变你，只是希望你能看到真实的自己。"
    },
    "权谋对话": {
        "structure": ["试探", "博弈", "让步/进攻", "达成/破裂"],
        "tone": "暗流涌动",
        "techniques": ["话中有话", "以退为进", "虚虚实实", "借力打力"],
        "example": "这天下，从来都不是一个人的天下。（意味深长地笑）"
    },
    "日常对话": {
        "structure": ["引入", "发展", "笑点/温馨点", "收尾"],
        "tone": "轻松、自然",
        "techniques": ["口癖", "吐槽", "互怼", "暖心"],
        "example": "你又在发呆了？（叹气）算了，习惯了。"
    },
    "战斗对话": {
        "structure": ["宣言", "交锋", "危机", "逆转"],
        "tone": "热血、激烈",
        "techniques": ["短句", "气势", "自信", "绝境反击"],
        "example": "这一招，接好了！（气势全开）还没完呢！"
    }
}

# ============================================================
# 标题生成模板数据
# ============================================================

TITLE_PATTERNS = {
    "玄幻仙侠": {
        "patterns": [
            "{动词}{名词}",
            "{形容词}{名词}传",
            "{名词}之{名词}",
            "我在{地点}修{名词}",
            "从{起点}开始的{名词}之路"
        ],
        "hot_words": ["仙", "道", "帝", "神", "天", "剑", "龙", "凤", "玄", "灵", "万古", "不朽", "苍穹", "混沌"],
        "style": "大气、神秘、有力量感"
    },
    "都市现实": {
        "patterns": [
            "{身份}的{名词}",
            "我的{名词}不可能这么{形容词}",
            "从{事件}开始",
            "{时间}后我{动作}"
        ],
        "hot_words": ["重生", "逆袭", "崛起", "商战", "医神", "兵王", "神豪", "系统"],
        "style": "接地气、有代入感"
    },
    "游戏竞技": {
        "patterns": [
            "{游戏术语}之{名词}",
            "我在{游戏}里{动作}",
            "{称号}{名词}",
            "从{状态}到{状态}"
        ],
        "hot_words": ["竞技", "荣耀", "王者", "巅峰", "全职", "电竞", "网游", "副本"],
        "style": "热血、竞技感"
    },
    "悬疑推理": {
        "patterns": [
            "{名词}的秘密",
            "第{数字}次{事件}",
            "{时间}的{名词}",
            "谁{动作}了{名词}"
        ],
        "hot_words": ["谜", "暗", "影", "密室", "真相", "嫌疑人", "第七天", "无声"],
        "style": "神秘、悬疑感"
    }
}

# ============================================================
# 分类映射（用于内容分类）
# ============================================================

CONTENT_CLASSIFICATION_KEYWORDS = {
    "character_design": {
        "primary": ["角色", "人物", "主角", "配角", "反派", "性格", "人设"],
        "secondary": ["人物塑造", "角色设计", "角色弧线", "人物弧线", "角色成长", "角色设定"]
    },
    "plot_structure": {
        "primary": ["情节", "剧情", "故事线", "冲突", "悬念", "伏笔", "高潮"],
        "secondary": ["反转", "节奏", "叙事", "大纲", "故事结构", "情节设计", "剧情设计"]
    },
    "worldbuilding": {
        "primary": ["世界观", "设定", "魔法体系", "力量体系", "修炼体系", "种族"],
        "secondary": ["功法体系", "战力体系", "地理", "历史", "文明", "势力", "宗门", "境界"]
    },
    "writing_techniques": {
        "primary": ["写作", "技巧", "文笔", "描写", "叙事技巧", "写作技法"],
        "secondary": ["写作方法", "写作手法", "修辞", "文风", "视角", "开篇", "结尾", "过渡"]
    },
    "dialogue_generation": {
        "primary": ["对话", "台词", "语言", "口癖", "对白"],
        "secondary": ["对话写作", "对话技巧", "对话设计"]
    },
    "mythology": {
        "primary": ["神话", "传说", "典故", "原型"],
        "secondary": ["神话体系", "民间传说", "神话原型", "神话设定"]
    },
    "templates": {
        "primary": ["模板", "公式", "套路", "框架", "万能模板"],
        "secondary": ["写作模板", "创作模板", "模板套路", "爽点", "爆点", "金手指", "逆袭", "打脸"]
    },
    "genresearch": {
        "primary": ["玄幻", "仙侠", "都市", "科幻", "悬疑", "言情", "历史"],
        "secondary": ["军事", "游戏", "体育", "灵异", "同人", "系统", "重生", "穿越"]
    },
    "platform_guides": {
        "primary": ["平台", "签约", "投稿", "编辑", "推荐", "榜单"],
        "secondary": ["平台规则", "平台指南", "网文平台", "番茄", "起点", "七猫"]
    },
    "monetization": {
        "primary": ["盈利", "赚钱", "收入", "变现", "稿费", "收益", "版权"],
        "secondary": ["IP", "IP改编", "网文收入", "写作赚钱"]
    }
}
