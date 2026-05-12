@echo off
chcp 65001 >nul
REM =====================================================
REM  小说创作内容自动采集系统启动器 v3.0
REM =====================================================

setlocal enabledelayedexpansion

set "PYTHON_PATH=python"
set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%"

cd /d "%PROJECT_DIR%"

echo.
echo ====================================================
echo    小说创作内容自动采集系统 v3.0
echo ====================================================
echo.

REM 检查Python是否安装
if exist "%PYTHON_PATH%" (
    for /f "tokens=*" %%i in ('"%PYTHON_PATH%" --version 2^>^&1') do set "PYTHON_VERSION=%%i"
    echo [信息] Python版本: !PYTHON_VERSION!
) else (
    echo [警告] 未找到指定Python路径，尝试系统Python...
    set "PYTHON_PATH=python"
)

REM 尝试找到可用的Python
"%PYTHON_PATH%" --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请确保已安装Python 3.7或更高版本
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo.

REM 检查必要文件
if not exist "config.py" (
    echo [错误] 找不到配置文件: config.py
    pause
    exit /b 1
)

if not exist "scripts\auto_content_collector.py" (
    echo [错误] 找不到采集脚本: scripts\auto_content_collector.py
    pause
    exit /b 1
)

if not exist "scripts\task_scheduler.py" (
    echo [错误] 找不到调度器: scripts\task_scheduler.py
    pause
    exit /b 1
)

if not exist "scripts\knowledge_importer.py" (
    echo [警告] 找不到知识录入器: scripts\knowledge_importer.py
)

echo [信息] 必要文件检查完成
echo.

REM 显示主菜单
:menu
echo.
echo 请选择操作:
echo.
echo   ── 采集任务 ──────────────────────
echo   1. 立即执行采集任务
echo   2. 查看任务状态
echo   3. 查看执行历史
echo.
echo   ── 调度管理 ──────────────────────
echo   4. 更新调度时间
echo   5. 创建Windows计划任务
echo   6. 启用任务
echo   7. 禁用任务
echo.
echo   ── 知识库管理 ────────────────────
echo   8. 打开知识库文件夹
echo   9. 打开日志文件夹
echo   A. 运行知识录入测试
echo.
echo   ── 其他 ──────────────────────────
echo   0. 退出
echo.
echo ====================================================
set /p choice=请输入选项:

if "%choice%"=="1" goto run_task
if "%choice%"=="2" goto show_status
if "%choice%"=="3" goto show_history
if "%choice%"=="4" goto update_schedule
if "%choice%"=="5" goto create_task
if "%choice%"=="6" goto enable_task
if "%choice%"=="7" goto disable_task
if "%choice%"=="8" goto open_kb
if "%choice%"=="9" goto open_logs
if /i "%choice%"=="a" goto run_importer_test
if "%choice%"=="0" goto end

echo.
echo [错误] 无效的选项，请重新选择
echo.
goto menu

:run_task
echo.
echo [信息] 正在执行采集任务...
echo.
"%PYTHON_PATH%" scripts\auto_content_collector.py
echo.
pause
goto menu

:show_status
echo.
"%PYTHON_PATH%" scripts\task_scheduler.py status
echo.
pause
goto menu

:show_history
echo.
set /p limit=请输入要查看的历史记录数量 [默认10]:
if "!limit!"=="" set limit=10
echo.
"%PYTHON_PATH%" scripts\task_scheduler.py history -n !limit!
echo.
pause
goto menu

:update_schedule
echo.
echo 请选择调度类型:
echo   1. 每天执行
echo   2. 每周执行
echo   3. 每月执行
echo   0. 返回
echo.
set /p sched_type=请输入选项 [0-3]:

if "!sched_type!"=="1" (
    set /p hour=请输入小时 (0-23):
    set /p minute=请输入分钟 (0-59):
    "%PYTHON_PATH%" scripts\task_scheduler.py update daily !hour! !minute!
) else if "!sched_type!"=="2" (
    echo 请选择星期:
    echo   1. 周一  2. 周二  3. 周三  4. 周四  5. 周五  6. 周六  7. 周日
    set /p day_num=请输入选项 [1-7]:
    set "day=周一"
    if "!day_num!"=="2" set "day=周二"
    if "!day_num!"=="3" set "day=周三"
    if "!day_num!"=="4" set "day=周四"
    if "!day_num!"=="5" set "day=周五"
    if "!day_num!"=="6" set "day=周六"
    if "!day_num!"=="7" set "day=周日"
    set /p hour=请输入小时 (0-23):
    set /p minute=请输入分钟 (0-59):
    "%PYTHON_PATH%" scripts\task_scheduler.py update weekly !day! !hour! !minute!
) else if "!sched_type!"=="3" (
    set /p hour=请输入小时 (0-23):
    set /p minute=请输入分钟 (0-59):
    "%PYTHON_PATH%" scripts\task_scheduler.py update monthly !hour! !minute!
) else (
    goto menu
)
echo.
pause
goto menu

:create_task
echo.
echo [信息] 正在创建Windows计划任务...
"%PYTHON_PATH%" scripts\task_scheduler.py windows-task
echo.
pause
goto menu

:enable_task
echo.
"%PYTHON_PATH%" scripts\task_scheduler.py enable
echo.
pause
goto menu

:disable_task
echo.
"%PYTHON_PATH%" scripts\task_scheduler.py disable
echo.
pause
goto menu

:open_kb
echo.
start explorer "%PROJECT_DIR%\knowledge"
echo [信息] 已打开知识库文件夹
goto menu

:open_logs
echo.
if exist "%PROJECT_DIR%\logs" (
    start explorer "%PROJECT_DIR%\logs"
    echo [信息] 已打开日志文件夹
) else (
    echo [信息] 日志文件夹不存在
)
goto menu

:run_importer_test
echo.
echo [信息] 正在运行知识录入系统测试...
echo.
"%PYTHON_PATH%" scripts\knowledge_importer.py
echo.
pause
goto menu

:end
echo.
echo ====================================================
echo    感谢使用！
echo ====================================================
echo.
exit /b 0
