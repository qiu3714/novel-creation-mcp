#!/usr/bin/env python3
"""
小说自动拆书脚本 v1.0
功能：自动分析小说文本，提取世界观、力量体系、势力、角色等信息，并整合到知识库
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class BookAnalysis:
    """小说分析结果"""
    id: str
    name: str
    author: str
    category: str
    core_positioning: str
    world_features: Dict[str, Any]
    power_system: Dict[str, Any]
    golden_finger_system: Dict[str, Any]
    character_archetypes: List[Dict[str, Any]]
    faction_systems: List[Dict[str, Any]]
    unique_settings: List[str]
    success_factors: List[str]
    writing_techniques: List[str]
    lessons: List[str]
    plot_structure: Dict[str, Any]


class NovelAnalyzer:
    """小说分析器"""

    def __init__(self, text: str, filename: str):
        self.text = text
        self.filename = filename
        self.lines = text.split('\n')
        self.chapters = self._extract_chapters()
        self.title = self._extract_title()
        self.author = self._extract_author()

    def _extract_title(self) -> str:
        """提取书名"""
        patterns = [
            r'^第?\s*【?\s*书名[：:]\s*(.+)',
            r'^(.+?)\s*作者[：:]\s*.+',
            r'《(.+?)》',
            r'"(.+?)"'
        ]
        for line in self.lines[:50]:
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    return match.group(1).strip()
        return self.filename.replace('.txt', '')

    def _extract_author(self) -> str:
        """提取作者"""
        patterns = [
            r'作者[：:]\s*(.+)',
            r'by\s*(.+)',
        ]
        for line in self.lines[:50]:
            for pattern in patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
        return "未知"

    def _extract_chapters(self) -> List[Dict[str, Any]]:
        """提取章节信息"""
        chapters = []
        chapter_pattern = r'^第?\s*【?\s*第?\s*([零一二三四五六七八九十百千0-9]+)\s*[章回部]?\s*】?\s*(.+)?'
        current_chapter = None
        current_content = []

        for i, line in enumerate(self.lines):
            match = re.match(chapter_pattern, line.strip())
            if match:
                if current_chapter:
                    current_chapter['content'] = '\n'.join(current_content)
                    current_chapter['line_count'] = len(current_content)
                    chapters.append(current_chapter)

                chapter_num = match.group(1)
                chapter_title = match.group(2) if match.group(2) else ""
                current_chapter = {
                    'number': chapter_num,
                    'title': chapter_title.strip(),
                    'line_start': i,
                    'content': '',
                    'content_preview': line
                }
                current_content = []
            else:
                if current_chapter:
                    current_content.append(line)

        if current_chapter:
            current_chapter['content'] = '\n'.join(current_content)
            current_chapter['line_count'] = len(current_content)
            chapters.append(current_chapter)

        return chapters

    def _extract_realm_levels(self) -> List[Dict[str, str]]:
        """提取修炼境界"""
        realms = []
        realm_patterns = [
            r'([零一二三四五六七八九十百千]+)\s*阶?',
            r'([\u4e00-\u9fa5]+)\s*境',
            r'阶段[一二三四五六七八九十\d]+',
            r'(炼体|锻体|玉筋|金身|神海|神宫|天人|半神|神级|凡人|凡人|修士|仙人|大帝|至尊)'
        ]

        realm_keywords = [
            '一阶', '二阶', '三阶', '四阶', '五阶', '六阶', '七阶', '八阶', '九阶',
            '锻体境', '玉筋境', '金身境', '神海境', '神宫境', '天人境',
            '半神', '神级', '凡人', '炼气', '筑基', '金丹', '元婴', '化神',
            '大乘', '渡劫', '真仙', '金仙', '太乙', '大罗', '混元', '圣人',
            '武帝', '武圣', '武神', '武尊', '武皇', '武宗', '武王', '武师'
        ]

        found_realms = set()
        for line in self.lines[:500]:
            for keyword in realm_keywords:
                if keyword in line and keyword not in found_realms:
                    found_realms.add(keyword)
                    realms.append({'name': keyword, 'description': self._get_context(line, keyword)})

        return realms

    def _extract_cultivation_system(self) -> Dict[str, Any]:
        """提取修炼体系"""
        system = {
            'cultivation_levels': [],
            'martial_arts': [],
            'talent_grades': []
        }

        talent_keywords = ['S级', 'A级', 'B级', 'C级', 'D级', 'E级', 'SSS', 'SS']
        for line in self.lines[:500]:
            for keyword in talent_keywords:
                if keyword in line:
                    system['talent_grades'].append({
                        'keyword': keyword,
                        'context': self._get_context(line, keyword)
                    })

        return system

    def _extract_characters(self) -> List[Dict[str, Any]]:
        """提取角色信息"""
        characters = []
        character_names = set()

        name_patterns = [
            r'([\u4e00-\u9fa5]{2,4})(?:说|道|笑|道：|说：|笑道)',
            r'主角[：:]\s*([\u4e00-\u9fa5]{2,4})',
            r'男主[：:]\s*([\u4e00-\u9fa5]{2,4})',
            r'([\u4e00-\u9fa5]{2,4})(?:是|被称为|成为)(?:主角|男主|主人公)',
        ]

        for line in self.lines[:1000]:
            for pattern in name_patterns:
                matches = re.findall(pattern, line)
                for name in matches:
                    if len(name) >= 2 and len(name) <= 4 and name not in character_names:
                        if not any(skip in name for skip in ['主角', '男主', '说道', '人说', '谁说']):
                            character_names.add(name)

                            role_type = self._infer_role_type(line, name)
                            characters.append({
                                'name': name,
                                'role': role_type,
                                'features': self._extract_character_features(line),
                                'first_appearance': self._get_context(line, name)
                            })

                            if len(characters) >= 20:
                                return characters

        return characters

    def _infer_role_type(self, line: str, name: str) -> str:
        """推断角色类型"""
        if any(keyword in line for keyword in ['主角', '男主', '主人公']):
            return '主角'
        elif any(keyword in line for keyword in ['反派', '敌人', 'BOSS']):
            return '反派'
        elif any(keyword in line for keyword in ['师父', '师傅', '老师', '长辈']):
            return '师父/长辈'
        elif any(keyword in line for keyword in ['队友', '伙伴', '兄弟', '闺蜜']):
            return '队友/伙伴'
        elif any(keyword in line for keyword in ['青梅竹马', '女主', '女主']):
            return '女主/情感线'
        else:
            return '配角'

    def _extract_character_features(self, line: str) -> List[str]:
        """提取角色特征"""
        features = []
        feature_keywords = [
            '天才', '废柴', '系统', '穿越', '重生', '冷静', '热血',
            '腹黑', '高冷', '傲娇', '霸气', '猥琐', '果断', '狠辣',
            '善良', '邪恶', '聪明', '愚蠢', '强大', '弱小'
        ]
        for keyword in feature_keywords:
            if keyword in self.text[:50000]:
                features.append(keyword)
        return list(set(features))[:5]

    def _extract_world_settings(self) -> Dict[str, Any]:
        """提取世界观设定"""
        world = {
            'setting': '',
            'education_system': '',
            'social_structure': '',
            'threats': '',
            'geography': '',
            'factions': []
        }

        settings_keywords = {
            'world': ['世界', '大陆', '星球', '位面', '仙界', '神界', '凡界'],
            'system': ['学院', '宗门', '家族', '王朝', '帝国', '学校'],
            'level': ['玄幻', '都市', '仙侠', '武侠', '科幻', '高武', '低武'],
            'threat': ['异兽', '魔兽', '妖兽', '魔族', '外敌', '天灾']
        }

        for category, keywords in settings_keywords.items():
            for keyword in keywords:
                if keyword in self.text[:100000]:
                    context = self._get_context_around_keyword(keyword, window=200)
                    if category == 'world' and not world['setting']:
                        world['setting'] = context[:200]
                    elif category == 'threat' and not world['threats']:
                        world['threats'] = context[:200]

        return world

    def _extract_golden_finger(self) -> Dict[str, Any]:
        """提取金手指系统"""
        golden_finger = {
            'name': '',
            'type': '',
            'mechanism': '',
            'features': []
        }

        system_keywords = ['系统', '金手指', '外挂', '异能', '天赋', '能力']
        for keyword in system_keywords:
            if keyword in self.text[:50000]:
                context = self._get_context_around_keyword(keyword, window=500)
                if not golden_finger['name']:
                    golden_finger['name'] = keyword
                    golden_finger['mechanism'] = context[:300]

        return golden_finger

    def _extract_plot_structure(self) -> Dict[str, Any]:
        """提取故事结构"""
        structure = {
            'starting_point': '',
            'core_conflict': '',
            'main_arc': []
        }

        if self.chapters:
            structure['starting_point'] = self.chapters[0].get('content_preview', '')[:200]

        conflict_keywords = ['矛盾', '冲突', '阴谋', '仇恨', '复仇', '争夺']
        for keyword in conflict_keywords:
            if keyword in self.text[:50000]:
                structure['core_conflict'] = self._get_context_around_keyword(keyword, window=200)
                break

        return structure

    def _get_context(self, line: str, keyword: str, window: int = 50) -> str:
        """获取关键词上下文"""
        idx = line.find(keyword)
        if idx == -1:
            return ""
        start = max(0, idx - window)
        end = min(len(line), idx + len(keyword) + window)
        return line[start:end].strip()

    def _get_context_around_keyword(self, keyword: str, window: int = 200) -> str:
        """在整个文本中获取关键词周围的上下文"""
        idx = self.text.find(keyword)
        if idx == -1:
            return ""
        start = max(0, idx - window)
        end = min(len(self.text), idx + window)
        return self.text[start:end].strip()

    def analyze(self) -> BookAnalysis:
        """执行完整分析"""
        book_id = self._generate_book_id()

        return BookAnalysis(
            id=book_id,
            name=self.title,
            author=self.author,
            category=self._infer_category(),
            core_positioning=self._infer_positioning(),
            world_features=self._extract_world_settings(),
            power_system=self._extract_cultivation_system(),
            golden_finger_system=self._extract_golden_finger(),
            character_archetypes=self._extract_characters(),
            faction_systems=self._extract_factions(),
            unique_settings=self._extract_unique_settings(),
            success_factors=self._infer_success_factors(),
            writing_techniques=self._infer_writing_techniques(),
            lessons=self._infer_lessons(),
            plot_structure=self._extract_plot_structure()
        )

    def _generate_book_id(self) -> str:
        """生成书籍ID"""
        name_for_id = self.title.replace(' ', '_').replace('\n', '')
        return ''.join(c for c in name_for_id if c.isalnum() or c == '_')[:50]

    def _infer_category(self) -> str:
        """推断小说类别"""
        categories = {
            '都市': ['都市', '现代', '城市', '商业', '职场'],
            '玄幻': ['玄幻', '异世', '斗气', '魔法', '西幻'],
            '仙侠': ['仙侠', '修真', '修仙', '飞升', '金丹', '元婴'],
            '武侠': ['武侠', '江湖', '武林', '武功', '侠客'],
            '科幻': ['科幻', '星际', '未来', '科技', '星际'],
            '游戏': ['游戏', '虚拟', '电竞', '网游'],
            '历史': ['历史', '古代', '三国', '秦时', '大明'],
        }

        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in self.text[:50000]:
                    return category

        return '其他'

    def _infer_positioning(self) -> str:
        """推断核心定位"""
        positioning = []

        if '系统' in self.text[:50000]:
            positioning.append('系统流')
        if '穿越' in self.text[:50000]:
            positioning.append('穿越')
        if '重生' in self.text[:50000]:
            positioning.append('重生')
        if '爽文' in self.text[:50000]:
            positioning.append('爽文')
        if '无敌' in self.text[:50000]:
            positioning.append('无敌流')
        if '进化' in self.text[:50000]:
            positioning.append('进化流')

        return ' + '.join(positioning) if positioning else '待分类'

    def _extract_factions(self) -> List[Dict[str, Any]]:
        """提取势力信息"""
        factions = []

        faction_keywords = ['宗门', '学院', '家族', '王朝', '帝国', '组织', '门派', '帮派']
        found_factions = set()

        for line in self.lines[:500]:
            for keyword in faction_keywords:
                if keyword in line and keyword not in found_factions:
                    match = re.search(rf'([\u4e00-\u9fa5]*{keyword}[\u4e00-\u9fa5]*)', line)
                    if match:
                        faction_name = match.group(1)
                        if len(faction_name) >= 3 and len(faction_name) <= 10:
                            found_factions.add(faction_name)
                            factions.append({
                                'name': faction_name,
                                'type': keyword,
                                'description': self._get_context(line, faction_name)
                            })

                            if len(factions) >= 10:
                                return factions

        return factions

    def _extract_unique_settings(self) -> List[str]:
        """提取独特设定"""
        settings = []

        unique_keywords = [
            ('系统', '系统流设定'),
            ('金手指', '金手指设计'),
            ('穿越', '穿越设定'),
            ('重生', '重生设定'),
            ('异能', '异能设定'),
            ('血脉', '血脉设定'),
            ('炼丹', '炼丹体系'),
            ('炼器', '炼器体系'),
        ]

        for keyword, desc in unique_keywords:
            if keyword in self.text[:50000]:
                settings.append(desc)

        return list(set(settings))[:10]

    def _infer_success_factors(self) -> List[str]:
        """推断成功因素"""
        factors = []

        if '系统' in self.text[:50000]:
            factors.append('系统设定吸引读者')
        if '爽' in self.text[:50000]:
            factors.append('爽点密集')
        if '逆袭' in self.text[:50000]:
            factors.append('逆袭爽感')
        if '装逼' in self.text[:50000] or '打脸' in self.text[:50000]:
            factors.append('装逼打脸套路')

        return factors if factors else ['待分析']

    def _infer_writing_techniques(self) -> List[str]:
        """推断写作技法"""
        techniques = []

        tech_keywords = {
            '系统开篇': ['系统', '叮', '提示'],
            '爽文节奏': ['爽', '碾压', '秒杀'],
            '装逼打脸': ['装逼', '打脸', '打脸'],
            '热血升级': ['升级', '突破', '进阶'],
            '情感线': ['女主', '感情', '恋爱'],
        }

        for tech, keywords in tech_keywords.items():
            for keyword in keywords:
                if keyword in self.text[:50000]:
                    techniques.append(tech)
                    break

        return list(set(techniques))[:5]

    def _infer_lessons(self) -> List[str]:
        """推断可借鉴要点"""
        lessons = []

        if '系统' in self.text[:50000]:
            lessons.append('系统设计思路')
        if '修炼' in self.text[:50000]:
            lessons.append('修炼体系设计')
        if '势力' in self.text[:50000]:
            lessons.append('势力体系构建')
        if '角色' in self.text[:50000]:
            lessons.append('角色塑造方法')

        return lessons if lessons else ['待提炼']


class BookAnalysisReport:
    """生成拆书报告"""

    @staticmethod
    def generate_markdown_report(analysis: BookAnalysis) -> str:
        """生成Markdown格式报告"""
        report = f"""# 拆书报告：《{analysis.name}》

## 一、作品概述

| 项目 | 内容 |
|------|------|
| **书名** | {analysis.name} |
| **作者** | {analysis.author} |
| **类型** | {analysis.category} |
| **核心定位** | {analysis.core_positioning} |

## 二、世界观设定

"""

        for key, value in analysis.world_features.items():
            if value:
                report += f"**{key}**：{value[:200]}...\n\n"

        report += """
## 三、力量体系

"""

        if analysis.power_system.get('cultivation_levels'):
            report += "### 修炼境界\n\n"
            for level in analysis.power_system['cultivation_levels'][:10]:
                report += f"- {level.get('name', '未知')}\n"
            report += "\n"

        if analysis.power_system.get('talent_grades'):
            report += "### 天赋等级\n\n"
            for grade in analysis.power_system['talent_grades'][:10]:
                report += f"- {grade.get('keyword', '未知')}\n"
            report += "\n"

        report += """
## 四、金手指系统

"""
        gf = analysis.golden_finger_system
        report += f"""**系统名称**：{gf.get('name', '未知')}
**运作机制**：{gf.get('mechanism', '待分析')[:300]}...

"""

        report += """
## 五、角色图谱

"""
        for char in analysis.character_archetypes[:15]:
            report += f"""### {char.get('name', '未知')}（{char.get('role', '未知')}）

**特征**：{', '.join(char.get('features', [])[:5])}
**初登场**：{char.get('first_appearance', '')[:100]}...

"""

        report += """
## 六、势力系统

"""
        for faction in analysis.faction_systems[:10]:
            report += f"""### {faction.get('name', '未知')}（{faction.get('type', '未知')}）

{faction.get('description', '')[:200]}...

"""

        report += f"""
## 七、独特设定

"""
        for setting in analysis.unique_settings[:10]:
            report += f"- {setting}\n"

        report += f"""

## 八、成功因素

"""
        for factor in analysis.success_factors:
            report += f"- {factor}\n"

        report += f"""

## 九、写作技法

"""
        for tech in analysis.writing_techniques:
            report += f"- {tech}\n"

        report += f"""

## 十、可借鉴要点

"""
        for lesson in analysis.lessons:
            report += f"- {lesson}\n"

        return report


class KnowledgeBaseManager:
    """知识库管理器"""

    def __init__(self, kb_path: str):
        self.kb_path = kb_path
        self.kb_data = self._load_knowledge_base()

    def _load_knowledge_base(self) -> dict:
        """加载知识库"""
        if os.path.exists(self.kb_path):
            with open(self.kb_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'ip_case_studies': {'case_studies': []}}

    def add_book_analysis(self, analysis: BookAnalysis):
        """添加书籍分析到知识库"""
        case_study = {
            'id': analysis.id,
            'name': analysis.name,
            'category': analysis.category,
            'author': analysis.author,
            'core_positioning': analysis.core_positioning,
            'world_features': analysis.world_features,
            'power_system': analysis.power_system,
            'golden_finger_system': analysis.golden_finger_system,
            'character_archetypes': analysis.character_archetypes,
            'faction_systems': analysis.faction_systems,
            'unique_settings': analysis.unique_settings,
            'success_factors': analysis.success_factors,
            'writing_techniques': analysis.writing_techniques,
            'lessons': analysis.lessons,
            'plot_structure': analysis.plot_structure,
            'analysis_date': datetime.now().isoformat()
        }

        existing = [i for i, s in enumerate(self.kb_data['ip_case_studies']['case_studies'])
                    if s.get('id') == analysis.id]

        if existing:
            self.kb_data['ip_case_studies']['case_studies'][existing[0]] = case_study
            print(f"更新已有书籍：{analysis.name}")
        else:
            self.kb_data['ip_case_studies']['case_studies'].append(case_study)
            print(f"新增书籍：{analysis.name}")

    def save(self):
        """保存知识库"""
        with open(self.kb_path, 'w', encoding='utf-8') as f:
            json.dump(self.kb_data, f, ensure_ascii=False, indent=2)
        print(f"知识库已保存到：{self.kb_path}")


def process_novel_file(file_path: str, kb_path: str) -> Optional[BookAnalysis]:
    """处理单本小说"""
    print(f"\n{'='*60}")
    print(f"正在处理：{file_path}")
    print('='*60)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        print(f"文件大小：{len(text):,} 字符")
        print(f"行数：{len(text.split(chr(10))):,}")

        filename = os.path.basename(file_path)
        analyzer = NovelAnalyzer(text, filename)

        print(f"识别书名：{analyzer.title}")
        print(f"识别作者：{analyzer.author}")
        print(f"识别章节：{len(analyzer.chapters)} 章")

        analysis = analyzer.analyze()

        print(f"识别角色：{len(analysis.character_archetypes)} 个")
        print(f"识别势力：{len(analysis.faction_systems)} 个")

        kb_manager = KnowledgeBaseManager(kb_path)
        kb_manager.add_book_analysis(analysis)
        kb_manager.save()

        report = BookAnalysisReport.generate_markdown_report(analysis)
        report_path = file_path.replace('.txt', '_拆书报告.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存：{report_path}")

        return analysis

    except Exception as e:
        print(f"处理失败：{e}")
        import traceback
        traceback.print_exc()
        return None


def process_novel_folder(folder_path: str, kb_path: str):
    """批量处理文件夹中的小说"""
    print(f"\n扫描文件夹：{folder_path}")

    txt_files = list(Path(folder_path).glob('*.txt'))
    print(f"找到 {len(txt_files)} 个TXT文件\n")

    results = []
    for i, file_path in enumerate(txt_files, 1):
        print(f"\n[{i}/{len(txt_files)}]", end="")
        result = process_novel_file(str(file_path), kb_path)
        if result:
            results.append(result)

    print(f"\n{'='*60}")
    print(f"批量处理完成！")
    print(f"成功：{len(results)}/{len(txt_files)}")
    print('='*60)

    return results


if __name__ == '__main__':
    import sys

    if len(sys.argv) >= 2:
        folder_path = sys.argv[1]
    else:
        folder_path = str(Path(__file__).parent.parent.parent / '拆书专用' / '小说')

    kb_path = str(Path(__file__).parent.parent / 'knowledge' / 'knowledge-base.json')

    print(f"小说拆书自动化脚本 v1.0")
    print(f"小说文件夹：{folder_path}")
    print(f"知识库文件：{kb_path}")

    if os.path.isdir(folder_path):
        process_novel_folder(folder_path, kb_path)
    elif os.path.isfile(folder_path):
        process_novel_file(folder_path, kb_path)
    else:
        print(f"路径不存在：{folder_path}")
