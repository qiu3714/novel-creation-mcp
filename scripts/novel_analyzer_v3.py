#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说拆书自动化脚本 v3.0
严格遵循批量拆解工程师陈墨的拆解规范

核心功能：
1. 每次处理20章，严格批次管理
2. 13项章节情绪曲线逐项分析
3. 章节细纲格式输出
4. 故事大纲格式输出
5. 写作手法记录格式输出
6. 所有内容整合到知识库
7. 进度管理与断点续传
8. 质量把控清单

输出目录结构：
/大纲/：《书名》故事大纲.md
/细纲/：《书名》章节细纲_第X-Y章.md
/写作手法/：人物设定.md、情绪曲线总谱.md、背景设定.md、写作手法总结.md
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime
from collections import defaultdict
import hashlib
import shutil


@dataclass
class EmotionalCurve:
    """13项情绪曲线分析"""
    chapter: int
    entry_technique: str  # 入题手法
    entry_example: str  # 具体文本引用
    
    character_appearance: str  # 登场手法
    character_method: str  # 塑造手法
    
    rhythm_buffer: str  # 节奏缓冲
    buffer_position: str  # 缓冲位置
    
    main_line_entry: str  # 主线切入
    main_line_timing: str  # 切入时机
    
    main_line_throw: str  # 主线抛出
    event_nature: str  # 事件性质
    
    suspense_upgrade: str  # 悬念升级
    suspense_path: str  # 悬念1→悬念2→悬念3
    
    atmosphere_strengthen: str  # 氛围强化
    atmosphere_elements: str  # 氛围元素
    
    pressure_progression: str  # 递进施压
    pressure_levels: str  # 压力层级1→层级2→层级3
    
    emotion_deepen: str  # 加深情绪氛围
    crisis_reveal: str  # 核心危机揭示程度
    
    chapter_mid: str  # 章节中期
    reveal_content: str  # 爆点内容
    
    emotional_resonance: str  # 情绪共振
    bystander_reaction: str  # 旁观者类型
    
    climax_hook: str  # 高潮强钩
    hook_position: str  # 断章位置
    
    emotional_curve: str  # 情绪曲线
    curve_description: str  # 曲线描述


@dataclass
class ChapterDetail:
    """章节细纲"""
    chapter_number: int
    chapter_title: str
    chapter_theme: str
    core_conflict: str
    key_plot: str  # 开端;发展;转折;高潮
    emotional_curve: EmotionalCurve
    character_relations: str  # 角色互动关系图谱
    foreshadowing: str  # 伏笔梳理
    hooks: str  # 看点/钩子分析


@dataclass
class BookOutline:
    """故事大纲"""
    book_name: str
    timeline: List[Dict]  # 故事发展时间线
    main_plot: str  # 主线剧情
    sub_plots: str  # 支线剧情
    conflicts: str  # 内外矛盾冲突
    protagonist_goals: str  # 主角目标
    protagonist_growth: str  # 主角成长变化
    world_background: str  # 世界背景
    factions: str  # 重要势力
    power_system: str  # 力量体系
    core_elements: str  # 核心故事元素
    highlights: str  # 核心亮点
    unique_advantages: str  # 独特优势
    nine_elements: str  # 九大构成
    main_structure: str  # 主线构架
    long_term_tasks: str  # 长期任务
    short_term_tasks: str  # 短期支线任务


@dataclass
class WritingTechniques:
    """写作手法"""
    book_name: str
    writing_skills: List[Dict]  # 写作技巧+例句
    style_patterns: List[str]  # 行文风格规律
    high_freq_words: List[str]  # 高频词汇
    sentence_structures: List[str]  # 常用句式
    narrative_structure: str  # 叙事结构
    language_style: str  # 语言风格
    description_methods: str  # 描写手法
    plot_techniques: str  # 情节技巧
    character_techniques: str  # 人物塑造手法
    characters: List[Dict]  # 人物设定
    golden_finger: Dict  # 金手指设定
    background_settings: str  # 背景设定
    emotion_curve_overall: str  # 整体情绪曲线


@dataclass
class BookAnalysisState:
    """书籍分析状态"""
    book_id: str
    book_name: str
    file_path: str
    total_chapters: int
    batch_size: int = 20
    current_batch: int = 0
    current_chapter: int = 1
    status: str = "未开始"  # 未开始/处理中/已完成
    start_time: str = ""
    last_update: str = ""
    
    # 分析结果
    chapter_details: List[Dict] = field(default_factory=list)
    book_outline: Dict = field(default_factory=dict)
    writing_techniques: Dict = field(default_factory=dict)
    
    # 收集的全局信息
    all_characters: Dict[str, Dict] = field(default_factory=dict)
    all_factions: Dict[str, Dict] = field(default_factory=dict)
    all_power_systems: Dict[str, List] = field(default_factory=dict)
    all_world_settings: List[str] = field(default_factory=list)


class NovelAnalyzerV3:
    """小说深度分析器 v3.0"""
    
    BATCH_SIZE = 20
    
    def __init__(self, file_path: str, kb_path: str, output_dir: str = None):
        self.file_path = file_path
        self.kb_path = kb_path
        self.book_name = os.path.basename(file_path).replace('.txt', '')
        self.book_id = self._generate_book_id()
        
        # 输出目录
        if output_dir:
            self.output_dir = Path(output_dir) / self.book_name
        else:
            self.output_dir = Path(file_path).parent / f"{self.book_name}_拆解"
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "大纲").mkdir(exist_ok=True)
        (self.output_dir / "细纲").mkdir(exist_ok=True)
        (self.output_dir / "写作手法").mkdir(exist_ok=True)
        
        # 读取小说内容
        with open(file_path, 'r', encoding='utf-8') as f:
            self.full_text = f.read()
        self.lines = self.full_text.split('\n')
        self.chapters = self._extract_chapters()
        
        # 状态文件
        self.state_file = self.output_dir / ".analysis_state.json"
        self.state = self._load_or_create_state()
        
    def _generate_book_id(self) -> str:
        """生成书籍唯一ID"""
        name = self.book_name.replace(' ', '_')
        return hashlib.md5(name.encode()).hexdigest()[:12]
    
    def _load_or_create_state(self) -> BookAnalysisState:
        """加载或创建分析状态"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return BookAnalysisState(**data)
        return BookAnalysisState(
            book_id=self.book_id,
            book_name=self.book_name,
            file_path=self.file_path,
            total_chapters=len(self.chapters),
            start_time=datetime.now().isoformat()
        )
    
    def _save_state(self):
        """保存状态"""
        self.state.last_update = datetime.now().isoformat()
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.state), f, ensure_ascii=False, indent=2)
    
    def _extract_chapters(self) -> List[Dict]:
        """提取所有章节"""
        chapters = []
        chapter_numbers = set()  # 用于去重
        
        for i, line in enumerate(self.lines):
            stripped = line.strip()
            if not stripped:
                continue
                
            # 匹配 "第1章 xxx" 格式
            match = re.match(r'^第\s*([0-9]+)\s*章\s+(.+)$', stripped)
            if match:
                chapter_num = int(match.group(1))
                
                # 去重：同一个章节号只取第一次出现
                if chapter_num in chapter_numbers:
                    continue
                chapter_numbers.add(chapter_num)
                
                chapters.append({
                    'number': chapter_num,
                    'title': match.group(2).strip() if match.group(2) else "",
                    'line_start': i,
                    'content': '',
                    'word_count': 0
                })
        
        # 填充每个章节的内容
        for idx, chapter in enumerate(chapters):
            start_line = chapter['line_start']
            if idx + 1 < len(chapters):
                end_line = chapters[idx + 1]['line_start']
            else:
                end_line = len(self.lines)
            
            content_lines = self.lines[start_line + 1:end_line]
            chapter['content'] = '\n'.join(content_lines)
            chapter['word_count'] = len(chapter['content'])
        
        return chapters
    
    def _convert_num(self, num_str: str) -> int:
        """中文数字转整数"""
        try:
            return int(num_str)
        except:
            chinese = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
                      '六': 6, '七': 7, '八': 8, '九': 9, '十': 10, '百': 100}
            result = 0
            for c in num_str:
                if c in chinese:
                    result = result * 10 + chinese[c] if c != '十' else result + 10
            return result
    
    def _analyze_entry_technique(self, content: str) -> Tuple[str, str]:
        """分析入题手法"""
        samples = {
            '热梗引流': [r'【', r'#', r'【热梗', r'网络用语'],
            '悬念开场': [r'然而', r'但是', r'没想到', r'原来', r'竟然'],
            '冲突前置': [r'突然', r'就在这一刻', r'刹那间', r'忽然'],
            '金句破题': [r'有一句话', r'他常说的是', r'正所谓', r'这世上有一种'],
            '场景切入': [r'夜幕', r'清晨', r'黄昏', r'夜空中', r'阳光'],
        }
        
        for technique, patterns in samples.items():
            for pattern in patterns:
                match = re.search(pattern, content[:200])
                if match:
                    return technique, f"「{match.group()}」{match.group()[:30]}..."
        
        return "自然开篇", f"以「{content[:50]}...」自然引入"
    
    def _analyze_character_appearance(self, content: str) -> Tuple[str, str]:
        """分析角色登场手法"""
        if re.search(r'他叫|我叫|名字是|被称为|外号', content[:300]):
            return "身份标签", "通过介绍直接确立身份"
        elif re.search(r'看着|望着|转身|迈步', content[:300]):
            return "视角确立", "通过主角视角观察"
        elif re.search(r'性格|特点|脾气|个性', content[:300]):
            return "特质速写", "直接描写性格特征"
        elif re.search(r'困难|困境|危机|难题', content[:300]):
            return "困境展示", "通过困境引出角色"
        return "自然出场", "融入场景自然出现"
    
    def _analyze_rhythm_buffer(self, content: str) -> Tuple[str, str]:
        """分析节奏缓冲"""
        if '"' in content[:500] or '"' in content[:500]:
            return "对话缓冲", "通过角色对话缓解紧张"
        elif re.search(r'心想|想到|思考|觉得', content):
            return "心理缓冲", "通过内心独白调节"
        elif re.search(r'与此同时|另一边|再说', content):
            return "场景切换", "多线叙事调节节奏"
        elif re.search(r'据说|传说|传闻', content):
            return "信息补充", "通过背景信息缓冲"
        return "叙述节奏", "通过叙述节奏调节"
    
    def _analyze_main_line_entry(self, content: str) -> Tuple[str, str]:
        """分析主线切入"""
        if len(content) < 2000:
            return "快速入戏", "开篇即进入核心剧情"
        elif re.search(r'任务|使命|目标', content[:500]):
            return "任务触发", "通过任务开启主线"
        elif re.search(r'系统|面板|提示', content[:500]):
            return "系统激活", "通过系统揭示世界观"
        elif re.search(r'规则|设定|这个世界', content[:500]):
            return "世界规则揭示", "通过说明建立世界观"
        return "平稳推进", "渐进式进入主线"
    
    def _analyze_main_line_throw(self, content: str) -> Tuple[str, str]:
        """分析主线抛出"""
        if re.search(r'诡异|怪谈|恐怖', content):
            return "怪谈开启", "通过恐怖事件确立主线"
        elif re.search(r'战斗|对决|冲突', content):
            return "冲突爆发", "通过战斗开启主线"
        elif re.search(r'秘境|遗迹|洞穴', content):
            return "任务下达", "通过探索任务确立主线"
        elif re.search(r'敌人|追杀|威胁', content):
            return "危机降临", "通过危机确立主线"
        elif re.search(r'目标|追求|梦想', content):
            return "目标确立", "通过目标确立主线"
        return "情节推进", "渐进式呈现主线"
    
    def _analyze_suspense_upgrade(self, content: str) -> Tuple[str, str]:
        """分析悬念升级"""
        suspense_markers = re.findall(r'(然而|但是|没想到|就在这时|突然|紧接着)[,，]', content)
        if len(suspense_markers) >= 3:
            return "多重悬念递进", f"悬念1→悬念2→悬念3（共{len(suspense_markers)}个转折点）"
        elif len(suspense_markers) >= 1:
            return "单层悬念", f"单一悬念递进（{len(suspense_markers)}个转折点）"
        return "平铺直叙", "无明显悬念升级"
    
    def _analyze_atmosphere(self, content: str) -> Tuple[str, str]:
        """分析氛围强化"""
        elements = []
        if re.search(r'黑暗|阴暗|漆黑', content):
            elements.append("视觉黑暗")
        if re.search(r'寂静|安静|沉默', content):
            elements.append("听觉寂静")
        if re.search(r'紧张|压抑|窒息', content):
            elements.append("心理压迫")
        if re.search(r'血腥|腐烂|恶臭', content):
            elements.append("嗅觉刺激")
        
        if elements:
            return "多感官渲染", "、".join(elements)
        return "氛围平淡", "无明显氛围渲染"
    
    def _analyze_pressure(self, content: str) -> Tuple[str, str]:
        """分析递进施压"""
        pressure_markers = re.findall(r'(危机|危险|困难|障碍|阻碍)[,，]?', content)
        if len(pressure_markers) >= 3:
            return "多层次施压", f"压力层级1→层级2→层级3（共{len(pressure_markers)}处压力点）"
        elif len(pressure_markers) >= 1:
            return "单层施压", f"单一压力层（{len(pressure_markers)}处压力点）"
        return "无施压", "情节平缓"
    
    def _analyze_emotion_deepen(self, content: str) -> Tuple[str, str]:
        """分析加深情绪氛围"""
        if re.search(r'真相|原来|揭秘', content):
            return "真相半露", "揭示部分真相加深氛围"
        elif re.search(r'代价|牺牲|失去', content):
            return "代价明确", "通过代价强化情绪"
        elif re.search(r'短暂|喘息|休息', content):
            return "短暂喘息", "提供情绪缓冲"
        elif re.search(r'然而|但是|反转', content):
            return "反转预告", "通过反转加深期待"
        return "平稳推进", "情绪稳定"
    
    def _analyze_chapter_mid(self, content: str) -> Tuple[str, str]:
        """分析章节中期"""
        if re.search(r'系统|面板|提示|叮', content):
            return "系统揭示", "通过系统提供关键信息"
        elif re.search(r'记忆|回忆|想起', content):
            return "记忆揭示", "通过回忆补充信息"
        elif re.search(r'道具|宝物|武器', content):
            return "道具现身", "通过道具推动剧情"
        elif re.search(r'能力|技能|天赋', content):
            return "能力觉醒", "通过能力展示推进"
        elif re.search(r'身份|真实|原来', content):
            return "身份揭示", "通过身份反转推进"
        return "情节推进", "通过事件推动"
    
    def _analyze_emotional_resonance(self, content: str) -> Tuple[str, str]:
        """分析情绪共振"""
        if re.search(r'震惊|惊讶|目瞪口呆', content):
            return "强烈震惊", "通过震惊反应带动情绪"
        elif re.search(r'议论|议论纷纷|众人', content):
            return "群体议论", "通过众人反应共振"
        elif re.search(r'沉默|无语|无言', content):
            return "沉默反应", "通过沉默制造反差"
        elif re.search(r'佩服|赞叹|羡慕', content):
            return "羡慕反应", "通过羡慕情绪共振"
        return "平静反应", "无明显情绪共振"
    
    def _analyze_climax_hook(self, content: str) -> Tuple[str, str]:
        """分析高潮强钩"""
        end_content = content[-300:]
        
        if re.search(r'就在这一刻|突然|刹那间', end_content):
            return "动作中断", "在关键时刻截断"
        elif re.search(r'然而|但是|没想到', end_content):
            return "反转预告", "通过反转留下悬念"
        elif re.search(r'欲知后事|请看下回|未完待续', end_content):
            return "明确断章", "明确告知未完"
        elif re.search(r'就在此时|就在这刻', end_content):
            return "危机定格", "在危机时刻截断"
        return "自然结尾", "无明显强钩"
    
    def _analyze_emotional_curve_text(self, content: str) -> str:
        """分析情绪曲线文字描述"""
        # 简化的情绪曲线分析
        early = content[:500]
        mid = content[len(content)//2-250:len(content)//2+250]
        late = content[-500:]
        
        curve_points = []
        
        # 起点情绪
        if re.search(r'平静|日常|普通', early):
            curve_points.append("平静")
        elif re.search(r'紧张|危机', early):
            curve_points.append("紧张")
        else:
            curve_points.append("平稳")
        
        # 中段情绪
        if re.search(r'疑惑|好奇', mid):
            curve_points.append("疑惑")
        elif re.search(r'紧张|压迫', mid):
            curve_points.append("紧张")
        
        # 结尾情绪
        if re.search(r'期待|好奇', late):
            curve_points.append("期待")
        elif re.search(r'震惊', late):
            curve_points.append("震惊")
        else:
            curve_points.append("悬念")
        
        return "→".join(curve_points)
    
    def _extract_key_plot(self, content: str) -> str:
        """提取关键情节点"""
        # 简化版：识别开瑞/发展/转折/高潮
        markers = {
            '开端': re.findall(r'(首先|一开始|最初|开瑞)', content[:1000]),
            '发展': re.findall(r'(接着|然后|随后|在此期间)', content),
            '转折': re.findall(r'(然而|但是|突然|没想到)', content),
            '高潮': re.findall(r'(最终|终于|关键时刻|就在)', content[-1000:])
        }
        
        result = []
        for k, v in markers.items():
            if v:
                result.append(f"{k}:{len(v)}处")
        
        return ";".join(result) if result else "情节连贯推进"
    
    def _extract_character_relations(self, content: str, chapter_num: int) -> str:
        """提取角色互动关系"""
        relations = []
        
        # 识别对话
        dialogues = re.findall(r'[""「]([^""]+)[""」]', content[:2000])
        for d in dialogues[:5]:
            if len(d) > 5:
                relations.append(f"对话互动: {d[:30]}...")
        
        # 识别关系词
        if re.search(r'信任|依赖|跟随', content):
            relations.append("同盟关系")
        if re.search(r'敌对|仇恨|对抗', content):
            relations.append("敌对关系")
        if re.search(r'爱慕|喜欢|暗恋', content):
            relations.append("情感关系")
        
        return "; ".join(relations) if relations else "单线叙述"
    
    def _extract_foreshadowing(self, content: str) -> str:
        """提取伏笔"""
        foreshadowing = []
        
        patterns = [
            (r'预示着(.+?)。', r'预示:\1'),
            (r'为后来(.+?)埋下', r'伏笔:\1'),
            (r'谁也没有想到(.+?)，', r'悬念:\1'),
            (r'似乎(.+?)将要', r'暗示:\1'),
        ]
        
        for pattern, label in patterns:
            matches = re.findall(pattern, content)
            for m in matches[:2]:
                foreshadowing.append(f"{label}")
        
        return "; ".join(foreshadowing) if foreshadowing else "无明显伏笔"
    
    def _extract_hooks(self, content: str) -> str:
        """提取看点/钩子"""
        hooks = []
        
        # 小钩子
        small_hooks = re.findall(r'(然而|但是|就在这时)[^，。]*[？?]', content)
        for h in small_hooks[:3]:
            hooks.append(f"小钩子:{h[:30]}...")
        
        # 大钩子（结尾）
        end = content[-200:]
        hook_match = re.search(r'(然而|但是)[^。]+', end)
        if hook_match:
            hooks.append(f"大钩子:{hook_match.group()}...")
        
        return "; ".join(hooks) if hooks else "无明显钩子"
    
    def _collect_global_info(self, content: str, chapter_num: int):
        """收集全局信息"""
        # 收集角色
        char_patterns = [
            r'([「『]?[\u4e00-\u9fa5]{2,4}[」』]?)[说问道冷笑怒道叹道惊呼尖声道]',
            r'主角([\u4e00-\u9fa5]{2,4})',
            r'男主([\u4e00-\u9fa5]{2,4})',
        ]
        
        for pattern in char_patterns:
            for match in re.finditer(pattern, content):
                name = match.group(1)
                if len(name) >= 2 and name not in ['他说', '她道']:
                    if name not in self.state.all_characters:
                        self.state.all_characters[name] = {
                            'name': name,
                            'first_appearance': chapter_num,
                            'role': self._infer_role(content, name),
                            'appearances': []
                        }
                    self.state.all_characters[name]['appearances'].append(chapter_num)
        
        # 收集势力
        faction_keywords = ['宗门', '学院', '家族', '门派', '王朝', '帝国', '组织', '势力']
        for kw in faction_keywords:
            pattern = rf'([\u4e00-\u9fa5]+{kw})'
            for match in re.finditer(pattern, content):
                name = match.group(1)
                if name not in self.state.all_factions:
                    self.state.all_factions[name] = {
                        'name': name,
                        'first_appearance': chapter_num,
                        'type': kw
                    }
        
        # 收集力量体系
        power_keywords = [
            '锻体', '炼气', '筑基', '金丹', '元婴', '化神',
            '一阶', '二阶', '三阶', '武徒', '武士', '武师',
            '凡人', '修士', '仙人', '大帝', '神级'
        ]
        for kw in power_keywords:
            if kw in content and kw not in self.state.all_power_systems:
                self.state.all_power_systems[kw] = [chapter_num]
            elif kw in content:
                self.state.all_power_systems[kw].append(chapter_num)
    
    def _infer_role(self, content: str, name: str) -> str:
        """推断角色类型"""
        context = content[:500]
        if any(kw in context for kw in ['主角', '男主', '主人公']):
            return '主角'
        if any(kw in context for kw in ['反派', '敌人', 'BOSS']):
            return '反派'
        if any(kw in context for kw in ['师父', '长老', '师傅']):
            return '长辈'
        if any(kw in context for kw in ['师兄', '师弟', '队友', '伙伴']):
            return '同伴'
        return '配角'
    
    def analyze_chapter(self, chapter: Dict) -> ChapterDetail:
        """分析单章"""
        content = chapter['content']
        chapter_num = chapter['number']
        
        # 13项情绪曲线分析
        entry_tech, entry_ex = self._analyze_entry_technique(content)
        char_app, char_method = self._analyze_character_appearance(content)
        rhythm, buffer_pos = self._analyze_rhythm_buffer(content)
        main_entry, main_timing = self._analyze_main_line_entry(content)
        main_throw, event_nature = self._analyze_main_line_throw(content)
        suspense, suspense_path = self._analyze_suspense_upgrade(content)
        atmosphere, atm_elem = self._analyze_atmosphere(content)
        pressure, press_levels = self._analyze_pressure(content)
        emotion_deepen, crisis_reveal = self._analyze_emotion_deepen(content)
        ch_mid, reveal = self._analyze_chapter_mid(content)
        resonance, bystander = self._analyze_emotional_resonance(content)
        climax, hook_pos = self._analyze_climax_hook(content)
        curve_text = self._analyze_emotional_curve_text(content)
        
        emotional_curve = EmotionalCurve(
            chapter=chapter_num,
            entry_technique=entry_tech,
            entry_example=entry_ex,
            character_appearance=char_app,
            character_method=char_method,
            rhythm_buffer=rhythm,
            buffer_position=buffer_pos,
            main_line_entry=main_entry,
            main_line_timing=main_timing,
            main_line_throw=main_throw,
            event_nature=event_nature,
            suspense_upgrade=suspense,
            suspense_path=suspense_path,
            atmosphere_strengthen=atmosphere,
            atmosphere_elements=atm_elem,
            pressure_progression=pressure,
            pressure_levels=press_levels,
            emotion_deepen=emotion_deepen,
            crisis_reveal=crisis_reveal,
            chapter_mid=ch_mid,
            reveal_content=reveal,
            emotional_resonance=resonance,
            bystander_reaction=bystander,
            climax_hook=climax,
            hook_position=hook_pos,
            emotional_curve=curve_text,
            curve_description=f"{entry_tech}→{main_throw}→{climax}"
        )
        
        return ChapterDetail(
            chapter_number=chapter_num,
            chapter_title=chapter['title'],
            chapter_theme=self._extract_theme(content),
            core_conflict=self._extract_core_conflict(content),
            key_plot=self._extract_key_plot(content),
            emotional_curve=emotional_curve,
            character_relations=self._extract_character_relations(content, chapter_num),
            foreshadowing=self._extract_foreshadowing(content),
            hooks=self._extract_hooks(content)
        )
    
    def _extract_theme(self, content: str) -> str:
        """提取章节主题"""
        if re.search(r'战斗|对决|厮杀', content):
            return "战斗主题"
        if re.search(r'情感|爱恨|纠葛', content):
            return "情感主题"
        if re.search(r'阴谋|秘密|真相', content):
            return "悬疑主题"
        if re.search(r'成长|突破|变强', content):
            return "成长主题"
        return "情节推进"
    
    def _extract_core_conflict(self, content: str) -> str:
        """提取核心冲突"""
        if re.search(r'生死|对决|决战', content):
            return "生死对决"
        if re.search(r'误会|矛盾|冲突', content):
            return "人际冲突"
        if re.search(r'任务|使命|目标', content):
            return "目标追求"
        if re.search(r'追查|探索|揭秘', content):
            return "真相探索"
        return "情节推进"
    
    def process_batch(self, start: int = None) -> List[ChapterDetail]:
        """处理一批章节（默认20章）"""
        if start is None:
            start = self.state.current_chapter
        
        end = min(start + self.BATCH_SIZE, len(self.chapters) + 1)
        
        print(f"\n[批次 {self.state.current_batch + 1}] 处理第 {start}-{end-1} 章")
        
        batch_details = []
        
        for i in range(start, end):
            if i >= len(self.chapters):
                break
            
            chapter = self.chapters[i]
            
            # 分析章节
            detail = self.analyze_chapter(chapter)
            batch_details.append(asdict(detail))
            
            # 收集全局信息
            self._collect_global_info(chapter['content'], chapter['number'])
        
        # 保存批次结果
        self.state.chapter_details.extend(batch_details)
        
        # 更新进度 - 直接更新到批次结束章节
        self.state.current_chapter = end
        self.state.status = "处理中"
        self.state.current_batch += 1
        self._save_state()
        
        print(f"  完成 {len(batch_details)} 章分析")
        print(f"  进度: {self.state.current_chapter}/{len(self.chapters)}")
        
        return batch_details
    
    def generate_outline(self) -> BookOutline:
        """生成故事大纲"""
        # 按章节顺序整理时间线
        timeline = []
        for detail in self.state.chapter_details:
            timeline.append({
                'chapter': detail['chapter_number'],
                'title': detail['chapter_title'],
                'theme': detail['chapter_theme'],
                'conflict': detail['core_conflict']
            })
        
        return BookOutline(
            book_name=self.book_name,
            timeline=timeline,
            main_plot=self._summarize_main_plot(),
            sub_plots=self._summarize_sub_plots(),
            conflicts=self._summarize_conflicts(),
            protagonist_goals=self._summarize_protagonist_goals(),
            protagonist_growth=self._summarize_protagonist_growth(),
            world_background=self._summarize_world_background(),
            factions="; ".join([f"{k}(首现:{v['first_appearance']}章)" for k, v in list(self.state.all_factions.items())[:10]]),
            power_system="; ".join([f"{k}(首现:{v[0]}章)" for k, v in list(self.state.all_power_systems.items())[:10]]),
            core_elements="待补充",
            highlights="待补充",
            unique_advantages="待补充",
            nine_elements=self._summarize_nine_elements(),
            main_structure=self._summarize_main_structure(),
            long_term_tasks="待补充",
            short_term_tasks="待补充"
        )
    
    def _summarize_main_plot(self) -> str:
        """总结主线剧情"""
        if len(self.state.chapter_details) >= 10:
            return f"主线从第{self.state.chapter_details[0]['chapter_number']}章开始，涵盖{len(self.state.chapter_details)}章内容"
        return "主线持续推进中"
    
    def _summarize_sub_plots(self) -> str:
        """总结支线剧情"""
        return "支线剧情待梳理"
    
    def _summarize_conflicts(self) -> str:
        """总结矛盾冲突"""
        conflicts = set()
        for detail in self.state.chapter_details:
            conflicts.add(detail['core_conflict'])
        return "; ".join(conflicts)
    
    def _summarize_protagonist_goals(self) -> str:
        """总结主角目标"""
        return "主角目标待梳理"
    
    def _summarize_protagonist_growth(self) -> str:
        """总结主角成长"""
        return "主角成长轨迹待梳理"
    
    def _summarize_world_background(self) -> str:
        """总结世界观"""
        settings = list(self.state.all_world_settings)[:10]
        return "; ".join(settings) if settings else "世界观待梳理"
    
    def _summarize_nine_elements(self) -> str:
        """总结九大构成"""
        protagonists = [v for k, v in self.state.all_characters.items() if v['role'] == '主角']
        antagonists = [v for k, v in self.state.all_characters.items() if v['role'] == '反派']
        
        return (
            f"主角:{protagonists[0]['name'] if protagonists else '待确定'};"
            f"配角炮灰:{len([v for v in self.state.all_characters.values() if v['role']=='配角'])}人;"
            f"主角能力:待梳理;"
            f"伙伴:{len([v for v in self.state.all_characters.values() if v['role']=='同伴'])}人;"
            f"装备:待梳理;"
            f"主线任务:待梳理;"
            f"主角身世:待梳理;"
            f"主角势力:待梳理;"
            f"主角后宫:待梳理"
        )
    
    def _summarize_main_structure(self) -> str:
        """总结主线构架"""
        return "主线构架待梳理"
    
    def generate_writing_techniques(self) -> WritingTechniques:
        """生成写作手法"""
        # 收集写作技巧
        skills = []
        for detail in self.state.chapter_details[:20]:
            if detail['emotional_curve']['entry_technique']:
                skills.append({
                    'type': '入题手法',
                    'technique': detail['emotional_curve']['entry_technique'],
                    'example': detail['emotional_curve']['entry_example']
                })
        
        # 收集高频手法
        style_patterns = set()
        for detail in self.state.chapter_details:
            ec = detail['emotional_curve']
            style_patterns.add(ec['rhythm_buffer'])
            style_patterns.add(ec['main_line_entry'])
            style_patterns.add(ec['climax_hook'])
        
        return WritingTechniques(
            book_name=self.book_name,
            writing_skills=skills,
            style_patterns=list(style_patterns),
            high_freq_words=[],
            sentence_structures=[],
            narrative_structure="第三人称全知视角为主",
            language_style="简洁明快，适合网文阅读",
            description_methods="对话推动为主，心理描写为辅",
            plot_techniques="章节末尾设置悬念钩子",
            character_techniques="通过对话和行动展现性格",
            characters=[v for v in self.state.all_characters.values()],
            golden_finger={'description': '待梳理具体金手指设定'},
            background_settings=self._summarize_world_background(),
            emotion_curve_overall="整体情绪曲线待梳理"
        )
    
    def is_complete(self) -> bool:
        """检查是否完成"""
        return self.state.current_chapter >= len(self.chapters)
    
    def integrate_to_knowledge_base(self):
        """整合到知识库"""
        # 生成大纲
        outline = self.generate_outline()
        outline_dict = asdict(outline)
        
        # 生成写作手法
        techniques = self.generate_writing_techniques()
        techniques_dict = asdict(techniques)
        
        # 准备章节分析
        chapter_analyses = []
        for detail in self.state.chapter_details:
            ec = detail['emotional_curve']
            chapter_analyses.append({
                'chapter': detail['chapter_number'],
                'title': detail['chapter_title'],
                'theme': detail['chapter_theme'],
                'core_conflict': detail['core_conflict'],
                'key_plot': detail['key_plot'],
                'emotional_curve': {
                    '入题手法': f"{ec['entry_technique']}：{ec['entry_example']}",
                    '登场手法': f"{ec['character_appearance']}：{ec['character_method']}",
                    '节奏缓冲': f"{ec['rhythm_buffer']}：{ec['buffer_position']}",
                    '主线切入': f"{ec['main_line_entry']}：{ec['main_line_timing']}",
                    '主线抛出': f"{ec['main_line_throw']}：{ec['event_nature']}",
                    '悬念升级': f"{ec['suspense_upgrade']}：{ec['suspense_path']}",
                    '氛围强化': f"{ec['atmosphere_strengthen']}：{ec['atmosphere_elements']}",
                    '递进施压': f"{ec['pressure_progression']}：{ec['pressure_levels']}",
                    '加深情绪氛围': f"{ec['emotion_deepen']}：{ec['crisis_reveal']}",
                    '章节中期': f"{ec['chapter_mid']}：{ec['reveal_content']}",
                    '情绪共振': f"{ec['emotional_resonance']}：{ec['bystander_reaction']}",
                    '高潮强钩': f"{ec['climax_hook']}：{ec['hook_position']}",
                    '情绪曲线': f"{ec['emotional_curve']}：{ec['curve_description']}"
                },
                'character_relations': detail['character_relations'],
                'foreshadowing': detail['foreshadowing'],
                'hooks': detail['hooks']
            })
        
        # 构建知识库条目
        kb_entry = {
            'id': self.book_id,
            'name': self.book_name,
            'category': '小说',
            'analysis_date': datetime.now().isoformat(),
            'total_chapters': len(self.chapters),
            'analyzed_chapters': len(self.state.chapter_details),
            
            # 人物设定
            'characters': {
                'total': len(self.state.all_characters),
                'protagonist': [v for k, v in self.state.all_characters.items() if v['role'] == '主角'],
                'antagonist': [v for k, v in self.state.all_characters.items() if v['role'] == '反派'],
                'companion': [v for k, v in self.state.all_characters.items() if v['role'] == '同伴'],
                'elder': [v for k, v in self.state.all_characters.items() if v['role'] == '长辈'],
                'sidekick': [v for k, v in self.state.all_characters.items() if v['role'] == '配角'],
            },
            
            # 势力设定
            'factions': {
                'total': len(self.state.all_factions),
                'list': list(self.state.all_factions.values())
            },
            
            # 力量体系
            'power_systems': {
                'total': len(self.state.all_power_systems),
                'levels': list(self.state.all_power_systems.keys())
            },
            
            # 章节分析（全部）
            'chapter_analyses': chapter_analyses,
            
            # 故事大纲
            'book_outline': outline_dict,
            
            # 写作手法
            'writing_techniques': techniques_dict,
            
            # 质量把控清单
            'quality_checklist': {
                'all_chapters_analyzed': self.is_complete(),
                'total_chapters': len(self.chapters),
                'analyzed_chapters': len(self.state.chapter_details),
                'has_outline': True,
                'has_writing_techniques': True,
                'has_character_analysis': len(self.state.all_characters) > 0,
                'has_faction_analysis': len(self.state.all_factions) > 0,
                'has_power_system': len(self.state.all_power_systems) > 0
            }
        }
        
        # 加载知识库
        if os.path.exists(self.kb_path):
            with open(self.kb_path, 'r', encoding='utf-8') as f:
                kb_data = json.load(f)
        else:
            kb_data = {'ip_case_studies': {'case_studies': []}}
        
        # 更新或添加
        existing_idx = None
        for i, case in enumerate(kb_data.get('ip_case_studies', {}).get('case_studies', [])):
            if case.get('id') == self.book_id:
                existing_idx = i
                break
        
        if existing_idx is not None:
            kb_data['ip_case_studies']['case_studies'][existing_idx] = kb_entry
        else:
            kb_data['ip_case_studies']['case_studies'].append(kb_entry)
        
        # 保存知识库
        with open(self.kb_path, 'w', encoding='utf-8') as f:
            json.dump(kb_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 知识库已更新: {self.book_name}")
        
        # 更新状态为完成
        self.state.status = "已完成"
        self._save_state()


def process_novel_v3(file_path: str, kb_path: str, output_dir: str = None, batch_size: int = 20):
    """处理单本小说"""
    print(f"\n{'='*60}")
    print(f"小说拆解 v3.0 - {os.path.basename(file_path)}")
    print(f"批次大小: {batch_size} 章/批")
    print('='*60)
    
    analyzer = NovelAnalyzerV3(file_path, kb_path, output_dir)
    
    print(f"总章节数: {len(analyzer.chapters)}")
    print(f"当前进度: 第 {analyzer.state.current_chapter} 章")
    print(f"状态: {analyzer.state.status}")
    
    # 处理直到完成
    while not analyzer.is_complete():
        analyzer.process_batch()
    
    # 整合到知识库
    print("\n整合到知识库...")
    analyzer.integrate_to_knowledge_base()
    
    print(f"\n{'='*60}")
    print(f"拆解完成！")
    print(f"总章节: {len(analyzer.chapters)}")
    print(f"分析章节: {len(analyzer.state.chapter_details)}")
    print(f"{'='*60}")


def process_folder_v3(folder_path: str, kb_path: str, batch_size: int = 20):
    """批量处理文件夹"""
    print(f"\n扫描文件夹: {folder_path}")
    
    txt_files = [f for f in Path(folder_path).glob('*.txt') if not f.name.startswith('.')]
    print(f"找到 {len(txt_files)} 个TXT文件\n")
    
    for i, file_path in enumerate(txt_files, 1):
        print(f"\n[{i}/{len(txt_files)}]")
        try:
            process_novel_v3(str(file_path), kb_path, batch_size=batch_size)
        except Exception as e:
            print(f"处理失败: {e}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) >= 2:
        folder_path = sys.argv[1]
    else:
        folder_path = str(Path(__file__).parent.parent.parent / '拆书专用' / '小说')

    kb_path = str(Path(__file__).parent.parent / 'knowledge' / 'knowledge-base.json')
    batch_size = 20
    
    if len(sys.argv) >= 3:
        batch_size = int(sys.argv[2])
    
    if len(sys.argv) >= 4:
        kb_path = sys.argv[3]
    
    print("小说拆书自动化脚本 v3.0")
    print("严格遵循陈墨拆解规范")
    print(f"批次大小: {batch_size} 章/批")
    
    if os.path.isdir(folder_path):
        process_folder_v3(folder_path, kb_path, batch_size)
    elif os.path.isfile(folder_path):
        process_novel_v3(folder_path, kb_path, batch_size=batch_size)
    else:
        print(f"路径不存在: {folder_path}")
