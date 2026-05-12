#!/usr/bin/env python3
import sys
import os

print('=' * 60)
print('MCP 服务器完整验证')
print('=' * 60)

print('\n[1/4] 检查 Python 环境...')
print(f'  Python 版本: {sys.version}')
print(f'  Python 路径: {sys.executable}')

print('\n[2/4] 检查 MCP 模块...')
try:
    import mcp
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    print('  MCP 模块已安装')
    print('  所有 MCP 组件导入成功')
except ImportError as e:
    print(f'  MCP 导入失败: {e}')
    sys.exit(1)

print('\n[3/4] 检查服务器文件...')
project_dir = os.path.dirname(os.path.abspath(__file__))
server_file = os.path.join(project_dir, 'server.py')
knowledge_file = os.path.join(project_dir, 'knowledge', 'knowledge-base.json')

if os.path.exists(server_file):
    print('  server.py 存在')
else:
    print('  server.py 不存在')
    sys.exit(1)

if os.path.exists(knowledge_file):
    size = os.path.getsize(knowledge_file) / 1024 / 1024
    print(f'  knowledge-base.json 存在 ({size:.2f} MB)')
else:
    print('  knowledge-base.json 不存在')
    sys.exit(1)

print('\n[4/4] 验证服务器代码...')
with open(server_file, 'r', encoding='utf-8') as f:
    content = f.read()

checks = [
    ('MCP 导入语句', 'from mcp.server import Server' in content),
    ('服务器启动函数', 'async def main():' in content),
    ('主程序入口', '__name__' in content and '__main__' in content),
    ('工具注册函数', 'list_tools' in content and 'call_tool' in content)
]

for name, passed in checks:
    status = 'PASS' if passed else 'FAIL'
    print(f'  {name}: [{status}]')

if all(check[1] for check in checks):
    print('\n' + '=' * 60)
    print('所有检查通过！MCP 服务器已准备就绪！')
    print('=' * 60)
    print('\n启动命令:')
    print(f'  cd "{project_dir}"')
    print('  python server.py')
else:
    print('\n部分检查失败，请检查服务器文件。')
    sys.exit(1)
