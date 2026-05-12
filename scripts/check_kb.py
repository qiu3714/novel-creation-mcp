#!/usr/bin/env python3
import json
import os
from pathlib import Path

kb_path = str(Path(__file__).parent.parent / 'knowledge' / 'knowledge-base.json')

with open(kb_path, 'r', encoding='utf-8') as f:
    kb = json.load(f)

size = len(json.dumps(kb))
content_count = len(kb.get("collected_content", []))

print(f"知识库大小: {size:,} 字符")
print(f"采集内容数量: {content_count} 条")
print(f"\n前5条采集内容:")
for i, item in enumerate(kb.get("collected_content", [])[:5], 1):
    print(f"{i}. {item.get('title', '无标题')[:50]}")
    print(f"   平台: {item.get('platform', '未知')} | 相关度: {item.get('relevance_score', 0)}%")
