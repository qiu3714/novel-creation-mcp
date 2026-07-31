# 小说创作 MCP 工具

一个基于 MCP (Model Context Protocol) 协议的小说创作辅助工具，提供角色设定、情节设计、世界观构建、写作技法和内容检索相关的工具接口。

## 发布状态

当前维护版本为 `3.0.0-rc.1` 候选版本。变更记录见 [CHANGELOG.md](CHANGELOG.md)，最新发布验收和社区证据状态见 [reports/release-readiness-2026-07-31.md](reports/release-readiness-2026-07-31.md)。正式 GitHub release 仍需要维护者确认来源风险范围并授权发布写入。

## 功能特性

### 12个核心工具

| 工具名称 | 功能描述 |
|---------|---------|
| `search_knowledge` | 在当前知识库中搜索写作技巧、角色设定、情节设计等内容 |
| `get_case_study` | 查询已记录且可再分发的案例分析 |
| `get_mythology` | 查询已记录的神话素材 |
| `get_template` | 获取已记录的设定或写作模板 |
| `get_methodology` | 获取系统化的写作方法论 |
| `generate_worldbuilding_prompt` | 生成完整的世界观设定框架提示词 |
| `analyze_power_system` | 分析力量体系的合理性并给出改进建议 |
| `generate_character` | AI辅助角色生成器，根据角色原型和题材生成设定框架 |
| `generate_plot` | AI辅助情节生成器，根据情节类型和题材生成情节框架 |
| `analyze_writing` | 写作质量分析器，分析文本的节奏、人物、对话、描写等 |
| `suggest_titles` | 标题/书名建议器，根据题材和主题生成标题建议 |
| `generate_dialogue` | AI辅助对话生成器，根据对话场景生成对话框架 |

## 当前公开内容范围

当前仓库注册了 12 个 MCP 工具。静态数据主要覆盖写作方法论、情节结构、世界观模板、角色原型、对话模板和标题模式。

`knowledge/knowledge-base.json` 与 `knowledge/collected_content.json` 保留了知识库结构和采集缓存结构，但当前公开快照没有可验证的外部采集条目，也没有可支撑固定数量的 IP 案例或神话体系数据。新增知识内容必须先满足 [CONTENT_POLICY.md](CONTENT_POLICY.md) 的来源记录要求。

## 安装方法

### 1. 创建虚拟环境并安装依赖

```bash
python -m venv .venv
# Windows PowerShell
.venv\\Scripts\\python -m pip install -r requirements.txt
```

依赖解析受 `constraints.txt` 约束；开发环境和 CI 都使用同一组版本边界。

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

更完整的 Windows、macOS 和 Linux stdio 配置示例见 [docs/MCP_CLIENT_SETUP.md](docs/MCP_CLIENT_SETUP.md)。

### 3. 启动服务器

```bash
python server.py
```

### 开发与验证

```bash
.venv\\Scripts\\python -m pip install -r requirements-dev.txt
.venv\\Scripts\\python -m pip check
.venv\\Scripts\\python -m compileall -q .
.venv\\Scripts\\python verify_setup.py
.venv\\Scripts\\python -m pytest -q
```

贡献、安全响应、行为准则和内容来源规则见 [CONTRIBUTING.md](CONTRIBUTING.md)、
[SECURITY.md](SECURITY.md)、[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) 与
[CONTENT_POLICY.md](CONTENT_POLICY.md)。

## 使用示例

### 搜索写作技巧

```
search_knowledge(query="如何写反派角色")
search_knowledge(query="伏笔设计", section="plot_structure")
```

### 获取IP案例分析

```
get_case_study(title="斗破苍穹")
```

### 获取神话体系

```
get_mythology(culture="希腊神话")
```

### 获取设定模板

```
get_template(template_type="力量体系")
```

### 获取写作方法论

```
get_methodology(topic="角色塑造")
get_methodology(topic="世界观构建")
```

### 生成世界观设定框架

```
generate_worldbuilding_prompt(world_type="修仙世界")
```

### 分析力量体系

```
analyze_power_system(system_description="以灵气为来源，分为炼气、筑基、结丹、元婴，突破需要资源并承担心魔风险。")
```

### 生成角色设定

```
generate_character(
    archetype="主角",
    genre="玄幻"
)
```

### 生成情节框架

```
generate_plot(
    plot_type="三幕结构",
    genre="悬疑"
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
    genre="玄幻仙侠",
    theme="命运轮回"
)
```

### 生成对话框架

```
generate_dialogue(
    scenario="冲突对话"
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

## 内容来源

本工具的知识条目必须遵守 [内容与来源政策](CONTENT_POLICY.md)。当前公开仓库不把未验证来源的第三方视频、字幕、课程、平台文章或受版权保护小说内容作为可再分发知识库发布。

历史来源线索和未解决风险记录在 [SOURCE_AUDIT.md](SOURCE_AUDIT.md)。新增公开知识条目前，必须记录来源 URL、许可或复用依据、检查日期和转化说明。

## 注意事项

- 本工具仅提供创作指导，不替代创作者的思考
- 不要将未验证来源、私稿、账号凭据或受版权保护的大段内容提交到公开知识库
- 力量体系分析结果仅供参考，最终设计由创作者决定

## License

MIT License
