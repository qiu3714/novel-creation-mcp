# 小说创作 MCP 工具

一个基于 MCP (Model Context Protocol) 协议的小说创作辅助工具，提供角色设定、情节设计、世界观构建、神话知识库、IP案例分析、写作技法等全方位创作指导。

## 功能特性

### 12个核心工具

| 工具名称 | 功能描述 |
|---------|---------|
| `search_knowledge` | 在知识库中搜索写作技巧、角色设定、情节设计等内容 |
| `get_case_study` | 获取11个顶级IP的世界观案例分析（诡秘之主、道诡异仙等） |
| `get_mythology` | 获取31个全球神话体系的详细信息 |
| `get_template` | 获取设定模板（力量体系、宗门架构、货币体系等） |
| `get_methodology` | 获取系统化的写作方法论 |
| `generate_worldbuilding_prompt` | 生成完整的世界观设定框架提示词 |
| `analyze_power_system` | 分析力量体系的合理性并给出改进建议 |
| `generate_character` | AI辅助角色生成器，根据角色类型、性格、背景生成设定框架 |
| `generate_plot` | AI辅助情节生成器，根据题材类型、结构模式生成情节框架 |
| `analyze_writing` | 写作质量分析器，分析文本的节奏、人物、对话、描写等 |
| `suggest_titles` | 标题/书名建议器，根据题材类型、关键词、风格生成标题建议 |
| `generate_dialogue` | AI辅助对话生成器，根据角色设定、场景生成对话框架 |

## 知识库内容

### 角色设定
- OC角色设定方法
- 女主人设设计
- 毒舌人设设计
- 反派角色设计（10大反派人设）
- 疯子角色写作指导
- 四种神性男主设计
- 人物情感写作体系（12种情感状态）
- 人物线与命运闭环设计

### 情节与结构
- 4种烧脑结构（时间循环/多线叙事/反转结构/嵌套结构）
- 伏笔与悬念设计（6种方法）
- 双线结构法
- 权谋与阴谋设计
- 九种爽点设计
- 名场面设计
- 两难结构设计
- 克苏鲁风格写作
- 无限流写作
- 开头十大毒点

### 世界观构建
- 架空世界三种类型
- 核心设定构建：四问法
- 势力范围构建：双国家关联法
- 七大核心体系
- 10条核心法则
- 世界观主要构成
- 常见设计误区

### 神话知识库
- 31个全球神话体系（欧洲/美洲/非洲/亚洲/大洋洲）
- 五大宇宙观分类（层级/循环/分离/漂浮/梦境）
- 跨文化神话原型
- 神话融合技巧

### IP案例分析
- 小说：诡秘之主、道诡异仙、凡人修仙传
- 游戏：艾尔登法环、黑暗之魂、赛博朋克2077、英雄联盟、巫师、原神
- 其他：战锤40K、指环王

### 写作技法
- 开篇写法（黄金三章）
- 代入感提升技巧
- 卖点设计
- BE美学写作
- 场景描写与氛围营造
- 冲突构建技巧
- 叙事视角与节奏控制
- 不同流派写作要点

## 安装方法

### 1. 创建虚拟环境并安装依赖

```bash
python -m venv .venv
# Windows PowerShell
.venv\\Scripts\\python -m pip install -r requirements.txt
```

### 2. 配置MCP客户端

在支持MCP的客户端（如Claude Desktop、Cursor等）中添加以下配置：

```json
{
  "mcpServers": {
    "novel-creation": {
      "command": "python",
      "args": [
        "/path/to/novel-creation-mcp/server.py"
      ]
    }
  }
}
```

> 请将 `/path/to/novel-creation-mcp/server.py` 替换为实际的项目路径。

### 3. 启动服务器

```bash
python server.py
```

### 开发与验证

```bash
.venv\\Scripts\\python -m pip install -r requirements-dev.txt
.venv\\Scripts\\python -m compileall -q .
.venv\\Scripts\\python verify_setup.py
.venv\\Scripts\\python -m pytest -q
```

贡献、安全响应和内容来源规则见 [CONTRIBUTING.md](CONTRIBUTING.md)、
[SECURITY.md](SECURITY.md) 与 [CONTENT_POLICY.md](CONTENT_POLICY.md)。

## 使用示例

### 搜索写作技巧

```
search_knowledge(query="如何写反派角色")
search_knowledge(query="伏笔设计", category="情节与结构")
```

### 获取IP案例分析

```
get_case_study(name="诡秘之主")
get_case_study()  # 获取所有IP列表
```

### 获取神话体系

```
get_mythology(name="希腊神话")
get_mythology(region="欧洲")
get_mythology()  # 获取所有神话体系概览
```

### 获取设定模板

```
get_template(name="力量体系")
get_template(name="宗门架构")
get_template()  # 获取所有模板列表
```

### 获取写作方法论

```
get_methodology(topic="角色塑造")
get_methodology(category="世界观构建")
get_methodology()  # 获取所有方法论概览
```

### 生成世界观设定框架

```
generate_worldbuilding_prompt(genre="奇幻", tone="严肃", power_level="中魔")
generate_worldbuilding_prompt(genre="修仙", focus_areas=["力量体系", "势力关系"])
```

### 分析力量体系

```
analyze_power_system(
    power_name="修仙体系",
    levels=["炼气", "筑基", "结丹", "元婴", "化神"],
    source="灵气",
    rules=["需要灵根", "需要资源", "有瓶颈"],
    costs=["消耗寿元", "有心魔风险"],
    social_impact="修仙者地位高于凡人"
)
```

### 生成角色设定

```
generate_character(
    role_type="主角",
    gender="男",
    personality="冷静",
    background="孤儿",
    traits=["理智", "善于分析", "外冷内热"]
)
```

### 生成情节框架

```
generate_plot(
    genre="悬疑",
    structure="悬疑反转",
    twists=3,
    themes=["复仇", "救赎", "真相"]
)
```

### 分析写作质量

```
analyze_writing(
    text="他站在窗前，望着外面的雨，心里充满了迷茫。不知道从什么时候开始，他觉得自己像一叶浮萍，在这个世界上漂荡，找不到方向。",
    focus="整体"
)
```

### 生成标题建议

```
suggest_titles(
    genre="奇幻",
    keywords=["魔法", "命运", "轮回"],
    style="文艺"
)
```

### 生成对话框架

```
generate_dialogue(
    character_a="主角",
    character_b="反派",
    context="在黑暗的密室中，两人对峙",
    purpose="制造冲突"
)
```

## 项目结构

```
novel-creation-mcp/
├── server.py                    # MCP服务器主文件（12个工具）
├── novel_data.py                # 静态数据模块（IP案例、神话、模板等）
├── config.py                    # 统一项目配置
├── start_server.py              # 服务器启动脚本（含预检）
├── verify_setup.py              # 环境验证脚本
├── start_collector.bat          # 内容采集系统启动器
├── requirements.txt             # Python依赖
├── README.md                    # 使用说明
├── README_自动化任务.md          # 采集系统文档
├── TROUBLESHOOTING.md           # 故障排除指南
├── scripts/
│   ├── auto_content_collector.py # 内容采集脚本
│   ├── task_scheduler.py         # 任务调度器
│   ├── knowledge_prompts.py      # 提示词系统
│   ├── knowledge_importer.py     # 智能知识录入
│   ├── auto_book_analyzer.py     # 小说拆书分析 v1
│   ├── novel_analyzer_v2.py      # 小说拆书分析 v2
│   ├── novel_analyzer_v3.py      # 小说拆书分析 v3
│   ├── check_kb.py               # 知识库检查工具
│   ├── test_system.py            # 系统测试脚本
│   └── task_config.json          # 调度配置
└── knowledge/
    ├── knowledge-base.json       # 知识库数据
    ├── collected_content.json    # 采集内容缓存
    ├── knowledge_prompts_config.json   # 提示词配置
    └── automation_prompts_config.json  # 自动化提示词配置
```

## 知识来源

本工具的知识条目必须遵守 [内容与来源政策](CONTENT_POLICY.md)。以下来源仅用于说明
研究方向；仓库不会镜像或重新发布原视频、字幕、课程或受版权保护的小说内容：
- **拆技巧合集**（尘三昧）：BE美学、碎片化叙事、意识流等
- **囤素材 抠设定合集**（尘三昧）：素材管理、世界观构建
- **神话地图合集**（馆长刘下饭）：30+全球神话体系
- **架空世界设计教程**（-waseyo-）：系统化世界观构建
- **小说世界构建教程**（狐面小说家）：七大核心体系、写作技法

## 注意事项

- 本工具仅提供创作指导，不替代创作者的思考
- 知识库内容来源于公开的教学视频整理
- 力量体系分析结果仅供参考，最终设计由创作者决定

## License

MIT License
