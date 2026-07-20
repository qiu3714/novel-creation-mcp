# 小说创作内容自动采集系统

## 📋 系统概述

本系统用于定期采集各大平台的小说创作相关内容，并整合到知识库中。

## 合规边界

采集配置中的平台名称不代表抓取、存储或再分发许可。任何准备提交到公开仓库的
知识条目，都必须先记录来源 URL、许可或复用依据、检查日期，以及对原内容做了
什么转化。缺少这些证据时，只能把线索记录为待审计风险，不能把采集结果并入公开
知识库。

## 📁 文件结构

```
novel-creation-mcp/
├── scripts/
│   ├── auto_content_collector.py   # 内容采集脚本 v2.1
│   ├── task_scheduler.py            # 任务调度器 v2.0
│   ├── task_config.json             # 调度配置
│   ├── collector_config.json        # 采集配置
│   └── check_kb.py                  # 知识库检查脚本
├── knowledge/
│   └── knowledge-base.json          # 知识库文件
├── logs/
│   └── collector.log                # 执行日志
├── content_report.md                # 采集报告
└── start_collector.bat             # 一键启动脚本
```

## 🚀 使用方法

### 方法1：双击启动（推荐）

1. 双击 `start_collector.bat`
2. 选择操作菜单中的选项

### 方法2：命令行执行

```bash
# 进入目录
cd novel-creation-mcp

# 查看任务状态
python scripts/task_scheduler.py status

# 立即执行采集任务
python scripts/task_scheduler.py run

# 改为每天执行（早上9点）
python scripts/task_scheduler.py update daily 9 0

# 改为每周执行（周三10:30）
python scripts/task_scheduler.py update weekly 周三 10 30
```

## ⚙️ 功能说明

### 1. 内容采集脚本 (auto_content_collector.py)

**功能**：
- 采集7个平台的内容：番茄小说、起点中文网、B站、抖音、知乎、微信公众号、小红书
- 智能去重
- 相关度评分
- 提取核心要点
- 自动更新知识库

**输出**：
- `knowledge/knowledge-base.json` - 知识库文件（包含采集内容）
- `content_report.md` - 采集报告
- `logs/collector.log` - 执行日志

### 2. 任务调度器 (task_scheduler.py)

**功能**：
- 管理任务执行
- 支持多种调度模式（每天/每周/每月）
- 记录执行历史
- 自动备份知识库

**命令**：
- `status` - 显示任务状态
- `run` - 立即执行任务
- `enable` - 启用任务
- `disable` - 禁用任务
- `history` - 显示执行历史
- `update` - 更新调度时间
- `windows-task` - 创建Windows计划任务

### 3. 知识库检查脚本 (check_kb.py)

**功能**：检查知识库状态

```bash
python scripts/check_kb.py
```

## 📊 采集平台

| 平台 | URL | 优先级 | 内容类型 |
|------|-----|--------|----------|
| 番茄小说 | tomatofiction.com | 高 | 教程、素材、经验分享 |
| 起点中文网 | qidian.com | 高 | 教程、专栏、访谈 |
| B站 | bilibili.com | 中 | 视频、教程、经验 |
| 抖音 | douyin.com | 中 | 短视频、文案、教程 |
| 知乎 | zhihu.com | 中 | 问答、专栏、经验 |
| 微信公众号 | mp.weixin.qq.com | 低 | 文章、教程、经验 |
| 小红书 | xiaohongshu.com | 低 | 笔记、教程 |

## ⚠️ 重要说明

### 关于知识库文件大小

知识库文件可能很大（超过20MB），这可能导致：
- 加载缓慢
- 内存占用高
- 部分工具无法完整读取

**优化措施**：
1. 脚本采用延迟加载机制，只在需要时才读取知识库
2. 采集内容只保存核心摘要（500字符）
3. 每条记录限制要点数量（10条）
4. 自动清理历史数据

### 建议

1. **定期备份**：在执行采集前，脚本会自动备份知识库
2. **监控大小**：如果知识库超过50MB，建议手动清理旧内容
3. **分批采集**：可以调整配置，只采集部分平台

## 🔧 配置说明

### 采集配置 (collector_config.json)

```json
{
    "max_items_per_platform": 10,
    "relevance_threshold": 0,
    "deduplication_enabled": true,
    "report_enabled": true,
    "platforms": [
        "番茄小说",
        "起点中文网",
        "B站",
        "抖音",
        "知乎",
        "微信公众号",
        "小红书"
    ],
    "keywords": [
        "小说创作",
        "写作技巧",
        "网文",
        "情节设计",
        "人物塑造",
        "世界观"
    ]
}
```

### 调度配置 (task_config.json)

```json
{
    "name": "小说创作内容自动采集",
    "schedule": {
        "type": "weekly",
        "day": "周一",
        "hour": 9,
        "minute": 0
    },
    "enabled": true,
    "settings": {
        "auto_backup": true,
        "max_history": 50,
        "retry_on_failure": true,
        "max_retries": 3
    }
}
```

## 📝 常见问题

### Q1: 提示"找不到Python"？

**解决方案**：
1. 确认Python已安装
2. 修改 `start_collector.bat` 中的 `PYTHON_PATH` 为正确的Python路径

### Q2: 知识库文件太大？

**解决方案**：
1. 手动清理 `knowledge/knowledge-base.json` 中的旧内容
2. 降低 `collector_config.json` 中的 `max_items_per_platform`
3. 减少 `platforms` 中的平台数量

### Q3: 采集内容重复？

**解决方案**：
确保 `collector_config.json` 中 `deduplication_enabled` 为 `true`

### Q4: 如何查看执行日志？

**解决方案**：
```bash
type logs\collector.log
```

或者双击 `start_collector.bat`，选择"9. 打开日志文件夹"

## 📞 联系方式

如有问题，请检查：
1. `logs/collector.log` - 执行日志
2. `content_report.md` - 采集报告
3. 知识库文件大小
