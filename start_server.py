#!/usr/bin/env python3
import sys
import asyncio

sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))

from config import (
    PYTHON_EXECUTABLE, KNOWLEDGE_BASE_FILE, MCP_SERVER_CONFIG,
    KNOWLEDGE_DIR, ensure_directories
)
from mcp.server.stdio import stdio_server


def preflight_check():
    print("=" * 50)
    print(f"  {MCP_SERVER_CONFIG['name']} v{MCP_SERVER_CONFIG['version']}")
    print("=" * 50)

    print(f"\n[1/4] Python 环境")
    print(f"  版本: {sys.version.split()[0]}")
    print(f"  路径: {sys.executable}")

    print(f"\n[2/4] MCP 模块")
    try:
        from mcp.server import Server
        from mcp.types import Tool, TextContent
        print("  OK - MCP 模块已就绪")
    except ImportError as e:
        print(f"  FAIL - MCP 模块导入失败: {e}")
        print("\n  解决方案:")
        print(f"    {PYTHON_EXECUTABLE} -m pip install mcp")
        sys.exit(1)

    print(f"\n[3/4] 知识库文件")
    if KNOWLEDGE_BASE_FILE.exists():
        size_kb = KNOWLEDGE_BASE_FILE.stat().st_size / 1024
        print(f"  OK - {KNOWLEDGE_BASE_FILE.name} ({size_kb:.1f} KB)")
    else:
        print(f"  WARN - 知识库文件不存在: {KNOWLEDGE_BASE_FILE}")
        print("  首次运行将自动创建")

    print(f"\n[4/4] 目录结构")
    ensure_directories()
    print("  OK - 所有必要目录已就绪")

    print("\n" + "=" * 50)
    print("启动 MCP 服务器...")
    print("=" * 50)
    print("\n服务器运行中，请保持此窗口打开。")
    print("按 Ctrl+C 可以停止服务器。\n")


async def main():
    from server import app
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    try:
        preflight_check()
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n服务器已停止。")
    except Exception as e:
        print(f"\n错误: {e}")
        input("\n按回车键退出...")
