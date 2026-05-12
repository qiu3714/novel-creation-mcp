#!/usr/bin/env python3
"""
测试采集系统 - 快速验证脚本
"""
import os
import sys

print("=" * 70)
print("小说创作内容自动采集系统 - 测试")
print("=" * 70)
print()

# 测试1: 检查Python版本
print("1. 检查Python环境...")
try:
    version = sys.version_info
    print(f"   ✓ Python版本: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 7:
        print("   ✓ Python版本符合要求")
    else:
        print("   ⚠ Python版本过低，建议使用Python 3.7+")
except Exception as e:
    print(f"   ✗ 检查失败: {e}")

print()

# 测试2: 检查必要文件
print("2. 检查必要文件...")
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)

required_files = [
    os.path.join(script_dir, 'auto_content_collector.py'),
    os.path.join(script_dir, 'task_scheduler.py'),
    os.path.join(project_dir, 'knowledge', 'knowledge-base.json')
]

for file_path in required_files:
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"   ✓ {os.path.basename(file_path)} ({size:,} bytes)")
    else:
        print(f"   ✗ 缺少文件: {os.path.basename(file_path)}")

print()

# 测试3: 检查知识库
print("3. 检查知识库...")
kb_path = os.path.join(project_dir, 'knowledge', 'knowledge-base.json')
if os.path.exists(kb_path):
    try:
        import json
        with open(kb_path, 'r', encoding='utf-8') as f:
            kb = json.load(f)

        content_count = len(kb.get('collected_content', []))
        total_items = kb.get('metadata', {}).get('total_items', 'N/A')

        print(f"   ✓ 知识库正常加载")
        print(f"   - 采集内容数量: {content_count} 条")
        print(f"   - 元数据记录: {total_items}")

        if content_count == 0:
            print("   ⚠ 知识库暂无采集内容，可以执行采集任务")
        else:
            print("   ✓ 知识库已有内容")

    except Exception as e:
        print(f"   ✗ 加载失败: {e}")
else:
    print(f"   ⚠ 知识库文件不存在，将自动创建")

print()

# 测试4: 检查目录权限
print("4. 检查目录权限...")
dirs_to_check = [
    project_dir,
    os.path.join(project_dir, 'knowledge'),
    os.path.join(project_dir, 'logs'),
    script_dir
]

for dir_path in dirs_to_check:
    if os.path.exists(dir_path):
        test_file = os.path.join(dir_path, '.write_test')
        try:
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            print(f"   ✓ {os.path.basename(dir_path)} 目录可写")
        except:
            print(f"   ⚠ {os.path.basename(dir_path)} 目录可能只读")
    else:
        print(f"   ⚠ 目录不存在: {os.path.basename(dir_path)}")

print()
print("=" * 70)
print("测试完成！")
print()
print("下一步：")
print("1. 双击 start_collector.bat 选择'立即执行采集任务'")
print("2. 或运行: python scripts/task_scheduler.py run")
print("=" * 70)
