# MCP 服务器故障排除指南

## 问题诊断

你遇到的错误是：`ModuleNotFoundError: No module named 'mcp'`

这意味着 Python 无法找到 `mcp` 模块。

---

## 解决方案（按顺序尝试）

### 方案 1：使用 python 命令（推荐）

```powershell
python -m pip install mcp
python server.py
```

### 方案 2：使用 py 命令

```powershell
py -m pip install mcp
py server.py
```

### 方案 3：检查所有 Python 版本

```powershell
py -0
```

然后使用指定版本：
```powershell
py -3.13 -m pip install mcp
py -3.13 server.py
```

### 方案 4：使用完整 Python 路径

```powershell
<your-python-path>\python.exe -m pip install mcp
<your-python-path>\python.exe server.py
```

---

## 验证安装

安装后，运行以下命令验证：

```powershell
python -c "from mcp.server import Server; print('MCP 安装成功！')"
```

---

## 完整启动流程

1. **打开 PowerShell 终端**
   - 按 `Win + X`，选择"Windows PowerShell"

2. **安装 MCP（如果还没安装）**
   ```powershell
   python -m pip install mcp
   ```

3. **启动服务器**
   ```powershell
   cd novel-creation-mcp
   python server.py
   ```

4. **验证服务器运行**
   - 如果服务器启动成功，它会等待连接，不会立即输出内容
   - 按 `Ctrl + C` 可以停止服务器

---

## 常见问题

### Q1: pip 不是内部或外部命令

**解决方案**：使用 `python -m pip` 而不是 `pip`

### Q2: 权限不足

**解决方案**：以管理员身份运行 PowerShell
1. 右键点击 PowerShell 图标
2. 选择"以管理员身份运行"

### Q3: 多个 Python 版本冲突

**解决方案**：明确指定要使用的 Python 版本
```powershell
py -0  # 查看所有可用版本
py -3.13 -m pip install mcp  # 指定版本安装
```

### Q4: MCP 模块安装在错误的 Python 版本

**解决方案**：确保安装和运行使用同一个 Python
```powershell
# 检查当前 Python
python -c "import sys; print(sys.executable)"

# 使用这个 Python 安装
<上面的路径> -m pip install mcp
```

---

## 自动诊断脚本

运行项目中的 `start_server.py` 脚本可以自动诊断问题：

```powershell
cd novel-creation-mcp
python start_server.py
```

这个脚本会：
1. 检测 Python 版本
2. 检查 MCP 模块是否可用
3. 验证知识库文件
4. 提供详细的错误信息

---

## 快速修复（最简单的方法）

如果以上都不行，复制以下命令到 PowerShell 终端：

```powershell
python -m pip install mcp --force-reinstall; cd novel-creation-mcp; python server.py
```

---

## 需要帮助？

如果仍然无法解决，请提供以下信息：
1. PowerShell 中的完整错误信息
2. `py -0` 的输出结果
3. `python -c "import sys; print(sys.version)"` 的输出结果
