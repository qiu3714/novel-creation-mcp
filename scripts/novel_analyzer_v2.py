#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说拆书自动化脚本 v2.0
严格遵循批量拆解工程师陈墨的拆书规范
功能：
1. 分批次处理（默认100章/批），确保连贯性
2. 生成13项章节情绪曲线分析
3. 提取世界观、力量体系、势力、角色等设定
4. 保存进度状态，支持断点续传
5. 生成完整细纲、大纲、写作手法文件
6. 最终整合到知识库
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


@dataclass
class ChapterAnalysis:
    """单章分析结果"""
    chapter_number: int
    chapter_title: str
    word_count: int
    core_conflict: str
    key_plot_points: List[str]
    emotional_curve: Dict[str, Any]
    characters_appeared: List[str]
    factions_appeared: List[str]
    world_settings: List[str]
    power_systems: List[str]
    foreshadowing: List[str]
    hooks: List[str]
    writing_techniques: List[str]


@dataclass
class BookState:
    """书籍处理状态"""
    book_id: str
    book_name: str
    total_chapters: int
    processed_chapters: int = 0
    current_batch: int = 0
    last_update: str = ""
    analysis_data: List[Dict] = field(default_factory=list)
    world_settings: Dict[str, Any] = field(default_factory=dict)
    character_map: Dict[str, Dict] = field(default_factory=dict)
    faction_map: Dict[str, Dict] = field(default_factory=dict)
    power_system: Dict[str, Any] = field(default_factory=dict)
    plot_summary: List[str] = field(default_factory=list)
    writing_techniques: List[str] = field(default_factory=list)


class NovelBookAnalyzer:
    """小说深度拆解器"""

    CHAPTER_BATCH_SIZE = 100  # 每批处理章节数

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.filename = os.path.basename(file_path)
        self.book_id = self._generate_book_id()
        self.state = self._load_or_create_state()

        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            self.full_text = f.read()
        self.lines = self.full_text.split('\n')
        self.chapters = self._extract_all_chapters()

    def _generate_book_id(self) -> str:
        """生成书籍唯一ID"""
        name_for_id = self.filename.replace('.txt', '').replace(' ', '_')
        return hashlib.md5(name_for_id.encode()).hexdigest()[:12]

    def _load_or_create_state(self) -> BookState:
        """加载或创建处理状态"""
        state_file = self._get_state_file()
        if state_file.exists():
            with open(state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return BookState(**data)
        else:
            return BookState(
                book_id=self.book_id,
                book_name=self.filename.replace('.txt', ''),
                total_chapters=0
            )

    def _get_state_file(self) -> Path:
        """获取状态文件路径"""
        return Path(self.file_path).parent / f".{self.book_id}_state.json"

    def _extract_all_chapters(self) -> List[Dict[str, Any]]:
        """提取所有章节"""
        chapters = []
        chapter_pattern = r'^第?\s*【?\s*第?\s*([零一二三四五六七八九十百千0-9]+)\s*[章回部]?\s*】?\s*(.+)?'

        current_chapter = None
        current_content = []

        for i, line in enumerate(self.lines):
            match = re.match(chapter_pattern, line.strip())
            if match:
                if current_chapter:
                    current_chapter['content'] = '\n'.join(current_content)
                    current_chapter['word_count'] = len(current_chapter['content'])
                    chapters.append(current_chapter)

                chapter_num = self._convert_chapter_number(match.group(1))
                chapter_title = match.group(2).strip() if match.group(2) else ""
                current_chapter = {
                    'number': chapter_num,
                    'title': chapter_title,
                    'line_start': i,
                    'content': '',
                    'word_count': 0
                }
                current_content = []
            else:
                if current_chapter:
                    current_content.append(line)

        if current_chapter:
            current_chapter['content'] = '\n'.join(current_content)
            current_chapter['word_count'] = len(current_chapter['content'])
            chapters.append(current_chapter)

        return chapters

    def _convert_chapter_number(self, num_str: str) -> int:
        """将中文数字转换为整数"""
        chinese_map = {
            '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
            '百': 100, '千': 1000
        }
        try:
            return int(num_str)
        except:
            return 0

    def _extract_entry_technique(self, content: str) -> str:
        """提取入题手法"""
        techniques = []
        if re.search(r'突然|忽然|就在这时|刹那间', content):
            techniques.append("冲突前置")
        if re.search(r'【|『|「', content):
            techniques.append("引号/符号开场")
        if re.search(r'原来|竟然|居然|没想到', content):
            techniques.append("悬念开场")
        if re.search(r'他|她|它|我', content[:200]):
            techniques.append("视角确立")
        return techniques[0] if techniques else "自然开篇"

    def _extract_character_appearance(self, content: str, chapter_num: int) -> List[Dict]:
        """提取角色登场信息"""
        characters = []
        # 匹配 "XXX说" "XXX道" "XXX冷笑" 等模式
        pattern = r'([「『]?[\u4e00-\u9fa5]{2,4}[」』]?)[说问道冷笑怒道怒喝道叹道惊呼尖声道]'
        matches = re.findall(pattern, content)
        for name in set(matches):
            if len(name) >= 2 and name not in ['他说', '她道']:
                characters.append({
                    'name': name,
                    'chapter': chapter_num,
                    'type': self._infer_character_type(content, name)
                })
        return characters

    def _infer_character_type(self, content: str, name: str) -> str:
        """推断角色类型"""
        if any(kw in content for kw in ['主角', '男主', '女主']):
            return '主角'
        if any(kw in content for kw in ['反派', '敌人', 'BOSS', '威胁']):
            return '反派'
        if any(kw in content for kw in ['师父', '师傅', '长老', '老师']):
            return '长辈/导师'
        if any(kw in content for kw in ['师兄', '师弟', '师姐', '师妹', '队友']):
            return '同伴'
        return '配角'

    def _extract_faction_info(self, content: str) -> List[str]:
        """提取势力信息"""
        factions = []
        faction_keywords = ['宗门', '学院', '家族', '门派', '王朝', '帝国', '组织', '势力', '帮派']
        for keyword in faction_keywords:
            pattern = rf'([\u4e00-\u9fa5]+{keyword})'
            matches = re.findall(pattern, content)
            factions.extend(matches)
        return list(set(factions))

    def _extract_world_settings(self, content: str) -> List[str]:
        """提取世界观设定"""
        settings = []
        setting_keywords = {
            '修炼': ['修炼', '功法', '境界', '突破', '修为'],
            '地理': ['大陆', '王国', '帝国', '城池', '城镇'],
            '社会': ['家族', '宗门', '门派', '王朝'],
            '力量': ['灵气', '魔力', '斗气', '真元']
        }
        for category, keywords in setting_keywords.items():
            for keyword in keywords:
                if keyword in content:
                    settings.append(f"{category}:{keyword}")
        return list(set(settings))

    def _extract_power_system(self, content: str) -> List[str]:
        """提取力量体系信息"""
        systems = []
        realm_keywords = [
            '锻体', '炼气', '筑基', '金丹', '元婴', '化神',
            '一阶', '二阶', '三阶', '武徒', '武士', '武师',
            '凡人', '修士', '仙人', '大帝', '神级'
        ]
        for keyword in realm_keywords:
            if keyword in content:
                systems.append(keyword)
        return systems

    def _extract_hooks(self, content: str, chapter_num: int) -> List[str]:
        """提取章节钩子"""
        hooks = []
        hook_patterns = {
            '悬念': r'但是|然而|不过|可是|就在这时',
            '危机': r'危险|危机|威胁|敌人|追杀',
            '转折': r'突然|竟然|原来|居然|没想到',
            '期待': r'终于|即将|很快|不久|接下来'
        }
        for hook_type, pattern in hook_patterns.items():
            if re.search(pattern, content):
                hooks.append(f"{hook_type}:{re.search(pattern, content).group()}")
        return hooks

    def _analyze_emotional_curve(self, content: str, chapter_num: int) -> Dict[str, Any]:
        """分析章节情绪曲线（13项分析）"""
        # 简化版情绪曲线分析
        curve = {
            'chapter': chapter_num,
            'entry_technique': self._extract_entry_technique(content),
            'character_appearance': len(re.findall(r'说|道|道：', content)),
            'rhythm_buffer': '对话' if '说' in content[:500] else '叙述',
            'main_line_entry': '快速' if chapter_num <= 3 else '平稳',
            'tension_buildup': self._calculate_tension_level(content),
            'suspense_upgrade': '有' if re.search(r'然而|但是|没想到', content) else '无',
            'atmosphere_intensity': self._calculate_atmosphere(content),
            'pressure_accumulation': len(re.findall(r'危险|危机|紧张', content)),
            'emotional_deepening': '递进' if chapter_num % 5 == 0 else '平稳',
            'mid_chapter_reveal': '关键信息' if re.search(r'原来|真相|秘密', content) else '情节推进',
            'emotional_resonance': '强烈' if re.search(r'震惊|惊呼|颤抖', content) else '一般',
            'climax_hook': '强钩' if re.search(r'就在这一刻|突然|刹那间', content[-200:]) else '普通'
        }
        return curve

    def _calculate_tension_level(self, content: str) -> str:
        """计算紧张度"""
        tension_words = len(re.findall(r'危险|危机|紧张|恐惧|担忧|害怕|死亡', content))
        if tension_words > 10:
            return '极高'
        elif tension_words > 5:
            return '高'
        elif tension_words > 2:
            return '中'
        return '低'

    def _calculate_atmosphere(self, content: str) -> str:
        """计算氛围强度"""
        atmosphere_words = len(re.findall(r'黑暗|冰冷|压抑|诡异|阴森|血腥|死亡', content))
        if atmosphere_words > 5:
            return '浓烈'
        elif atmosphere_words > 2:
            return '较强'
        return '平淡'

    def _extract_writing_techniques(self, content: str) -> List[str]:
        """提取写作技巧"""
        techniques = []

        # 对话描写
        if re.search(r'说.*道|道.*:', content):
            techniques.append("对话推进")

        # 心理描写
        if re.search(r'心想|想着|思考|觉得', content):
            techniques.append("心理描写")

        # 动作描写
        if re.search(r'转身|抬手|迈步|冲上前|后退', content):
            techniques.append("动作描写")

        # 环境描写
        if re.search(r'天空|大地|夜幕|阳光|风声', content):
            techniques.append("环境渲染")

        # 比喻
        if re.search(r'像|如|仿佛|如同', content):
            techniques.append("比喻修辞")

        return techniques

    def _extract_foreshadowing(self, content: str) -> List[str]:
        """提取伏笔"""
        foreshadowing = []
        patterns = [
            r'预示着',
            r'似乎.*将要',
            r'埋下了.*伏笔',
            r'这为后来',
            r'谁也没有想到'
        ]
        for pattern in patterns:
            if re.search(pattern, content):
                foreshadowing.append(re.search(pattern, content).group())
        return foreshadowing

    def analyze_batch(self, start_chapter: int, batch_size: int = None) -> List[ChapterAnalysis]:
        """分析一批章节"""
        if batch_size is None:
            batch_size = self.CHAPTER_BATCH_SIZE

        end_chapter = min(start_chapter + batch_size, len(self.chapters))
        batch_analyses = []

        print(f"  分析第 {start_chapter} - {end_chapter} 章...")

        for i in range(start_chapter, end_chapter):
            if i >= len(self.chapters):
                break

            chapter = self.chapters[i]
            content = chapter['content']

            analysis = ChapterAnalysis(
                chapter_number=chapter['number'],
                chapter_title=chapter['title'],
                word_count=chapter['word_count'],
                core_conflict=self._extract_core_conflict(content),
                key_plot_points=self._extract_key_points(content),
                emotional_curve=self._analyze_emotional_curve(content, chapter['number']),
                characters_appeared=[c['name'] for c in self._extract_character_appearance(content, chapter['number'])],
                factions_appeared=self._extract_faction_info(content),
                world_settings=self._extract_world_settings(content),
                power_systems=self._extract_power_system(content),
                foreshadowing=self._extract_foreshadowing(content),
                hooks=self._extract_hooks(content, chapter['number']),
                writing_techniques=self._extract_writing_techniques(content)
            )
            batch_analyses.append(analysis)

            # 更新全局状态
            self._update_global_state(chapter['number'], content, analysis)

        # 保存状态
        self._save_state()

        return batch_analyses

    def _extract_core_conflict(self, content: str) -> str:
        """提取核心冲突"""
        if re.search(r'战斗|对决|生死|危机|威胁', content):
            return "生死对决"
        elif re.search(r'误会|矛盾|冲突|争执', content):
            return "人际冲突"
        elif re.search(r'任务|使命|目标|追求', content):
            return "目标追求"
        elif re.search(r'秘密|真相|发现|揭示', content):
            return "真相探索"
        return "情节推进"

    def _extract_key_points(self, content: str) -> List[str]:
        """提取关键情节点"""
        points = []
        # 提取对话关键点
        dialogues = re.findall(r'["""](.+?)["""]', content)
        for d in dialogues[:3]:
            if len(d) > 10:
                points.append(d[:50])
        return points

    def _update_global_state(self, chapter_num: int, content: str, analysis: ChapterAnalysis):
        """更新全局状态"""
        # 更新已处理章节数
        self.state.processed_chapters = max(self.state.processed_chapters, chapter_num)

        # 更新角色映射
        for char_info in self._extract_character_appearance(content, chapter_num):
            name = char_info['name']
            if name not in self.state.character_map:
                self.state.character_map[name] = {
                    'name': name,
                    'first_appearance': chapter_num,
                    'type': char_info['type'],
                    'appearances': []
                }
            self.state.character_map[name]['appearances'].append(chapter_num)

        # 更新势力映射
        for faction in analysis.factions_appeared:
            if faction not in self.state.faction_map:
                self.state.faction_map[faction] = {
                    'name': faction,
                    'first_appearance': chapter_num
                }

        # 更新力量体系
        for system in analysis.power_systems:
            if system not in self.state.power_system:
                self.state.power_system[system] = chapter_num

        # 更新情节摘要
        if chapter_num % 10 == 0:
            self.state.plot_summary.append(f"第{chapter_num}章: {analysis.core_conflict}")

        # 更新写作技巧
        for tech in analysis.writing_techniques:
            if tech not in self.state.writing_techniques:
                self.state.writing_techniques.append(tech)

    def _save_state(self):
        """保存处理状态"""
        self.state.last_update = datetime.now().isoformat()
        state_file = self._get_state_file()
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.state), f, ensure_ascii=False, indent=2)

    def get_remaining_chapters(self) -> int:
        """获取剩余未处理章节数"""
        return len(self.chapters) - self.state.processed_chapters

    def is_complete(self) -> bool:
        """检查是否完成"""
        return self.state.processed_chapters >= len(self.chapters)

    def generate_full_report(self) -> Dict[str, Any]:
        """生成完整拆书报告"""
        report = {
            'metadata': {
                'book_id': self.book_id,
                'book_name': self.state.book_name,
                'total_chapters': len(self.chapters),
                'processed_chapters': self.state.processed_chapters,
                'analysis_date': datetime.now().isoformat()
            },
            'world_settings': self.state.world_settings,
            'character_analysis': {
                'total_characters': len(self.state.character_map),
                'characters': list(self.state.character_map.values())
            },
            'faction_analysis': {
                'total_factions': len(self.state.faction_map),
                'factions': list(self.state.faction_map.values())
            },
            'power_system_analysis': {
                'total_systems': len(self.state.power_system),
                'systems': self.state.power_system
            },
            'plot_summary': self.state.plot_summary,
            'writing_techniques': self.state.writing_techniques,
            'chapter_analyses': [
                asdict(a) for a in self._load_all_analyses()
            ]
        }
        return report

    def _load_all_analyses(self) -> List[ChapterAnalysis]:
        """加载所有已保存的分析"""
        analyses = []
        for i in range(0, len(self.chapters), self.CHAPTER_BATCH_SIZE):
            batch_file = self._get_batch_file(i)
            if batch_file.exists():
                with open(batch_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for d in data:
                        analyses.append(ChapterAnalysis(**d))
        return analyses

    def _get_batch_file(self, start_chapter: int) -> Path:
        """获取批次文件路径"""
        return Path(self.file_path).parent / f".{self.book_id}_batch_{start_chapter}.json"

    def save_batch_analysis(self, analyses: List[ChapterAnalysis], start_chapter: int):
        """保存批次分析"""
        batch_file = self._get_batch_file(start_chapter)
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(a) for a in analyses], f, ensure_ascii=False, indent=2)
        self.state.current_batch = start_chapter
        self._save_state()


class KnowledgeBaseIntegrator:
    """知识库整合器"""

    def __init__(self, kb_path: str):
        self.kb_path = kb_path
        self.kb_data = self._load_kb()

    def _load_kb(self) -> dict:
        """加载知识库"""
        if os.path.exists(self.kb_path):
            with open(self.kb_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'ip_case_studies': {'case_studies': []}}

    def integrate_book_report(self, report: Dict[str, Any]):
        """整合书籍报告到知识库"""
        # 检查是否已存在
        existing_idx = None
        for i, case in enumerate(self.kb_data.get('ip_case_studies', {}).get('case_studies', [])):
            if case.get('id') == report['metadata']['book_id']:
                existing_idx = i
                break

        # 构建案例数据
        case_data = {
            'id': report['metadata']['book_id'],
            'name': report['metadata']['book_name'],
            'category': '小说',
            'analysis_date': report['metadata']['analysis_date'],
            'total_chapters': report['metadata']['total_chapters'],
            'world_features': report['world_settings'],
            'character_analysis': report['character_analysis'],
            'faction_analysis': report['faction_analysis'],
            'power_system_analysis': report['power_system_analysis'],
            'plot_summary': report['plot_summary'],
            'writing_techniques': report['writing_techniques'],
            'chapter_sample_analysis': report['chapter_analyses'][:20]  # 只保存前20章样本
        }

        if existing_idx is not None:
            self.kb_data['ip_case_studies']['case_studies'][existing_idx] = case_data
            print(f"  更新已有案例: {case_data['name']}")
        else:
            self.kb_data['ip_case_studies']['case_studies'].append(case_data)
            print(f"  新增案例: {case_data['name']}")

        self._save_kb()

    def _save_kb(self):
        """保存知识库"""
        with open(self.kb_path, 'w', encoding='utf-8') as f:
            json.dump(self.kb_data, f, ensure_ascii=False, indent=2)
        print(f"  知识库已保存")


def process_book_novel(file_path: str, kb_path: str, batch_size: int = 100, auto_continue: bool = True):
    """处理单本小说"""
    print(f"\n{'='*60}")
    print(f"开始处理：{os.path.basename(file_path)}")
    print(f"批次大小：{batch_size} 章")
    print('='*60)

    analyzer = NovelBookAnalyzer(file_path)

    print(f"总章节数：{len(analyzer.chapters)}")
    print(f"已处理章节：{analyzer.state.processed_chapters}")

    # 分批处理
    start = analyzer.state.processed_chapters
    while start < len(analyzer.chapters):
        print(f"\n[批次 {start//batch_size + 1}]")
        analyses = analyzer.analyze_batch(start, batch_size)
        analyzer.save_batch_analysis(analyses, start)
        print(f"  完成 {len(analyses)} 章分析")
        print(f"  进度：{start + len(analyses)}/{len(analyzer.chapters)}")

        start += batch_size

        if not auto_continue and start < len(analyzer.chapters):
            print(f"\n  已暂停。可通过再次运行继续。")
            break

    # 生成完整报告
    print("\n生成完整拆书报告...")
    report = analyzer.generate_full_report()

    # 整合到知识库
    print("整合到知识库...")
    integrator = KnowledgeBaseIntegrator(kb_path)
    integrator.integrate_book_report(report)

    # 生成Markdown报告
    report_path = file_path.replace('.txt', '_完整拆书报告.md')
    generate_markdown_report(report, report_path)
    print(f"报告已保存：{report_path}")

    print(f"\n{'='*60}")
    print(f"处理完成！")
    print(f"{'='*60}")

    return report


def generate_markdown_report(report: Dict, output_path: str):
    """生成Markdown格式完整报告"""
    md = f"""# 完整拆书报告：{report['metadata']['book_name']}

## 基本信息

| 项目 | 内容 |
|------|------|
| 书名 | {report['metadata']['book_name']} |
| 总章节数 | {report['metadata']['total_chapters']} |
| 分析日期 | {report['metadata']['analysis_date']} |

## 角色分析

**总角色数**：{report['character_analysis']['total_characters']}

### 主要角色

"""

    # 添加主角
    protagonists = [c for c in report['character_analysis']['characters']
                    if c.get('type') == '主角']
    for char in protagonists[:5]:
        md += f"- **{char['name']}**（主角）- 首次出现：第{char['first_appearance']}章\n"

    md += f"""
### 配角

"""
    others = [c for c in report['character_analysis']['characters']
              if c.get('type') != '主角'][:10]
    for char in others:
        md += f"- {char['name']} - 首次出现：第{char['first_appearance']}章\n"

    md += f"""

## 势力分析

**总势力数**：{report['faction_analysis']['total_factions']}

"""
    for faction in report['faction_analysis']['factions'][:10]:
        md += f"- {faction['name']} - 首次出现：第{faction['first_appearance']}章\n"

    md += f"""

## 力量体系

"""
    for system, chapter in report['power_system_analysis']['systems'].items():
        md += f"- {system} - 首次出现：第{chapter}章\n"

    md += f"""

## 情节发展（每10章一记）

"""
    for summary in report['plot_summary']:
        md += f"- {summary}\n"

    md += f"""

## 写作技巧汇总

"""
    for tech in report['writing_techniques']:
        md += f"- {tech}\n"

    md += f"""

## 章节分析样本（前20章）

"""
    chapter_samples = report.get('chapter_sample_analysis', [])
    if chapter_samples:
        for chapter in chapter_samples[:20]:
            md += f"""

### 第{chapter['chapter_number']}章 {chapter['chapter_title']}

- **字数**：{chapter['word_count']}
- **核心冲突**：{chapter['core_conflict']}
- **情绪曲线**：{chapter['emotional_curve']}
- **登场角色**：{', '.join(chapter['characters_appeared'][:5])}
- **钩子**：{', '.join(chapter['hooks']) if chapter['hooks'] else '无'}

"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md)


def process_folder(folder_path: str, kb_path: str, batch_size: int = 100):
    """批量处理文件夹中的小说"""
    print(f"\n扫描文件夹：{folder_path}")

    txt_files = list(Path(folder_path).glob('*.txt'))
    txt_files = [f for f in txt_files if not f.name.startswith('.')]  # 排除临时文件

    print(f"找到 {len(txt_files)} 个TXT文件\n")

    results = []
    for i, file_path in enumerate(txt_files, 1):
        print(f"\n[{i}/{len(txt_files)}]")
        try:
            result = process_book_novel(str(file_path), kb_path, batch_size)
            results.append(result)
        except Exception as e:
            print(f"  处理失败：{e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'='*60}")
    print(f"批量处理完成！")
    print(f"成功：{len(results)}/{len(txt_files)}")
    print(f"{'='*60}")

    return results


if __name__ == '__main__':
    import sys

    if len(sys.argv) >= 2:
        folder_path = sys.argv[1]
    else:
        folder_path = str(Path(__file__).parent.parent.parent / '拆书专用' / '小说')

    kb_path = str(Path(__file__).parent.parent / 'knowledge' / 'knowledge-base.json')
    batch_size = 100

    if len(sys.argv) >= 3:
        batch_size = int(sys.argv[2])

    if len(sys.argv) >= 4:
        kb_path = sys.argv[3]

    print(f"小说拆书自动化脚本 v2.0")
    print(f"批次大小：{batch_size} 章/批")
    print(f"小说文件夹：{folder_path}")
    print(f"知识库文件：{kb_path}")

    if os.path.isdir(folder_path):
        process_folder(folder_path, kb_path, batch_size)
    elif os.path.isfile(folder_path):
        process_book_novel(folder_path, kb_path, batch_size)
    else:
        print(f"路径不存在：{folder_path}")
