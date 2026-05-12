"""
小说创作内容采集任务调度器 v3.0
================================
功能：管理和调度内容采集任务，支持定时执行、任务历史记录和多种调度模式
使用统一的 config.py 配置，避免重复定义
"""

import sys
import json
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import (
    SCHEDULER_CONFIG, PROJECT_ROOT, SCRIPTS_DIR, LOGS_DIR,
    BACKUPS_DIR, TASK_CONFIG_FILE, PYTHON_EXECUTABLE
)

DEFAULT_RUNTIME = {
    "last_run": None,
    "next_run": None,
    "run_count": 0,
    "success_count": 0,
    "fail_count": 0,
    "history": []
}


class TaskScheduler:

    def __init__(self):
        self.config = self._load_config()
        self._update_next_run()

    def _load_config(self) -> Dict[str, Any]:
        config = {**SCHEDULER_CONFIG, **DEFAULT_RUNTIME}
        if TASK_CONFIG_FILE.exists():
            try:
                with open(TASK_CONFIG_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                for key in SCHEDULER_CONFIG:
                    if key in saved:
                        config[key] = saved[key]
                for key in DEFAULT_RUNTIME:
                    if key in saved:
                        config[key] = saved[key]
            except Exception as e:
                print(f"加载配置失败: {e}，使用默认配置")
        return config

    def _save_config(self):
        try:
            TASK_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(TASK_CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")

    def _update_next_run(self):
        self.config["next_run"] = self.calculate_next_run().isoformat()

    def calculate_next_run(self) -> datetime:
        now = datetime.now()
        schedule = self.config.get("schedule", {})
        schedule_type = schedule.get("type", "weekly")
        target_hour = schedule.get("hour", 9)
        target_minute = schedule.get("minute", 0)

        if schedule_type == "daily":
            next_run = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(days=1)

        elif schedule_type == "weekly":
            day_map = {"周一": 0, "周二": 1, "周三": 2, "周四": 3,
                       "周五": 4, "周六": 5, "周日": 6}
            target_weekday = day_map.get(schedule.get("day", "周一"), 0)
            days_ahead = (target_weekday - now.weekday()) % 7
            if days_ahead == 0 and (now.hour > target_hour or
                                    (now.hour == target_hour and now.minute >= target_minute)):
                days_ahead = 7
            next_run = now + timedelta(days=days_ahead)
            next_run = next_run.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)

        elif schedule_type == "monthly":
            next_run = now.replace(day=1, hour=target_hour, minute=target_minute, second=0, microsecond=0)
            if next_run <= now:
                if now.month == 12:
                    next_run = next_run.replace(year=now.year + 1, month=1)
                else:
                    next_run = next_run.replace(month=now.month + 1)

        else:
            next_run = now + timedelta(days=(7 - now.weekday()) % 7)
            next_run = next_run.replace(hour=9, minute=0, second=0, microsecond=0)

        return next_run

    def _add_to_history(self, status: str, message: str, details: Optional[Dict] = None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "message": message,
            "details": details or {}
        }
        self.config["history"].insert(0, entry)
        max_history = self.config.get("settings", {}).get("max_history", 50)
        if len(self.config["history"]) > max_history:
            self.config["history"] = self.config["history"][:max_history]

    def _backup_knowledge_base(self):
        if not self.config.get("settings", {}).get("auto_backup", True):
            return None
        kb_path = PROJECT_ROOT / "knowledge" / "knowledge-base.json"
        if kb_path.exists():
            try:
                BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = BACKUPS_DIR / f"knowledge_base_{timestamp}.json"
                shutil.copy2(kb_path, backup_path)
                backups = sorted(BACKUPS_DIR.glob("knowledge_base_*.json"))
                while len(backups) > 10:
                    backups.pop(0).unlink()
                return backup_path
            except Exception as e:
                print(f"备份失败: {e}")
        return None

    def run_now(self, force: bool = False) -> bool:
        print(f"\n{'='*70}")
        print(f"开始执行任务")
        print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")

        start_time = datetime.now()

        try:
            backup_path = self._backup_knowledge_base()
            if backup_path:
                print(f"知识库已备份: {backup_path.name}")

            collector_path = SCRIPTS_DIR / "auto_content_collector.py"
            if not collector_path.exists():
                raise FileNotFoundError(f"采集脚本不存在: {collector_path}")

            print("正在执行采集任务...")
            print("-" * 70)

            result = subprocess.run(
                [PYTHON_EXECUTABLE, str(collector_path)],
                capture_output=True, text=True, encoding="utf-8", timeout=3600
            )

            duration = (datetime.now() - start_time).total_seconds()

            if result.returncode == 0:
                print("\n" + "-" * 70)
                print("任务执行成功！")
                print(f"执行耗时: {duration:.2f}秒")
                self.config["success_count"] += 1
                self.config["last_run"] = datetime.now().isoformat()
                self._add_to_history("success", "任务执行成功", {
                    "duration": duration,
                    "output_preview": result.stdout[:500] if result.stdout else ""
                })
            else:
                print("\n" + "-" * 70)
                print(f"任务执行失败！错误码: {result.returncode}")
                if result.stderr:
                    print(f"错误信息: {result.stderr[:500]}")
                self.config["fail_count"] += 1
                self.config["last_run"] = datetime.now().isoformat()
                self._add_to_history("failure", "任务执行失败", {
                    "error_code": result.returncode,
                    "error": result.stderr[:500] if result.stderr else ""
                })

            self.config["run_count"] += 1

        except subprocess.TimeoutExpired:
            print("\n任务执行超时（超过1小时）")
            self.config["fail_count"] += 1
            self._add_to_history("timeout", "任务执行超时")

        except FileNotFoundError as e:
            print(f"\n文件未找到: {e}")
            self.config["fail_count"] += 1
            self._add_to_history("error", str(e))

        except Exception as e:
            print(f"\n任务执行异常: {e}")
            self.config["fail_count"] += 1
            self._add_to_history("exception", str(e))

        finally:
            self._update_next_run()
            self._save_config()
            print(f"\n{'='*70}")
            next_run = datetime.fromisoformat(self.config["next_run"])
            print(f"下次执行: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*70}\n")

        return self.config["run_count"] > 0

    def check_and_run(self) -> bool:
        if not self.config.get("enabled", True):
            print("任务已禁用，跳过执行")
            return False

        now = datetime.now()
        try:
            next_run = datetime.fromisoformat(self.config["next_run"]) if self.config.get("next_run") else None
        except (ValueError, TypeError):
            next_run = None

        if not next_run:
            self._update_next_run()
            next_run = datetime.fromisoformat(self.config["next_run"])

        if abs((now - next_run).total_seconds()) <= 60:
            print("到达执行时间，正在执行任务...")
            return self.run_now()
        return False

    def _format_schedule_str(self) -> str:
        schedule = self.config.get("schedule", {})
        stype = schedule.get("type", "weekly")
        hour = schedule.get("hour", 9)
        minute = schedule.get("minute", 0)
        time_str = f"{hour}:{minute:02d}"

        if stype == "weekly":
            return f"每周{schedule.get('day', '周一')} {time_str}"
        elif stype == "daily":
            return f"每天 {time_str}"
        elif stype == "monthly":
            return f"每月1号 {time_str}"
        return f"每周一 {time_str}"

    def show_status(self):
        print("\n" + "=" * 70)
        print("任务调度器状态")
        print("=" * 70)
        print(f"任务名称: {self.config.get('name', '未命名')}")
        print(f"描述: {self.config.get('description', '')}")
        print(f"版本: {self.config.get('version', '1.0.0')}")
        print(f"状态: {'已启用' if self.config.get('enabled', True) else '已禁用'}")
        print("-" * 70)
        print(f"调度设置: {self._format_schedule_str()}")
        print("-" * 70)
        print("执行统计:")
        print(f"  总执行次数: {self.config.get('run_count', 0)}")
        print(f"  成功次数: {self.config.get('success_count', 0)}")
        print(f"  失败次数: {self.config.get('fail_count', 0)}")

        for label, key in [("上次执行", "last_run"), ("下次执行", "next_run")]:
            if self.config.get(key):
                try:
                    dt = datetime.fromisoformat(self.config[key])
                    print(f"  {label}: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                except (ValueError, TypeError):
                    print(f"  {label}: {self.config[key]}")

        history = self.config.get("history", [])
        if history:
            print("-" * 70)
            print("最近执行历史 (最近5次):")
            for i, entry in enumerate(history[:5], 1):
                try:
                    ts = datetime.fromisoformat(entry.get("timestamp", ""))
                    time_str = ts.strftime("%m-%d %H:%M")
                except (ValueError, TypeError):
                    time_str = entry.get("timestamp", "")[:10]
                icon = "OK" if entry.get("status") == "success" else "FAIL"
                print(f"  {i}. [{icon}] {time_str} - {entry.get('message', '')}")
        print("=" * 70)

    def show_history(self, limit: int = 10):
        history = self.config.get("history", [])
        if not history:
            print("暂无执行历史")
            return

        print("\n" + "=" * 70)
        print(f"执行历史 (共 {len(history)} 条记录，显示前 {limit} 条)")
        print("=" * 70)

        for i, entry in enumerate(history[:limit], 1):
            try:
                ts = datetime.fromisoformat(entry.get("timestamp", ""))
                time_str = ts.strftime("%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                time_str = entry.get("timestamp", "")

            status = entry.get("status", "")
            icon = {"success": "OK", "failure": "FAIL"}.get(status, "INFO")
            print(f"\n{i}. [{icon}] {time_str}")
            print(f"   状态: {entry.get('message', '')}")

            details = entry.get("details", {})
            if "duration" in details:
                print(f"   耗时: {details['duration']:.2f}秒")
            if "error" in details:
                print(f"   错误: {details['error'][:100]}...")
        print("\n" + "=" * 70)

    def enable(self):
        self.config["enabled"] = True
        self._update_next_run()
        self._save_config()
        print("任务已启用")

    def disable(self):
        self.config["enabled"] = False
        self._save_config()
        print("任务已禁用")

    def update_schedule(self, schedule_type: str = None, day: str = None, hour: int = None, minute: int = None):
        if schedule_type:
            self.config["schedule"]["type"] = schedule_type
        if day:
            self.config["schedule"]["day"] = day
        if hour is not None:
            self.config["schedule"]["hour"] = hour
        if minute is not None:
            self.config["schedule"]["minute"] = minute

        self._update_next_run()
        self._save_config()
        print(f"调度时间已更新为: {self._format_schedule_str()}")

    def reset_stats(self):
        self.config["run_count"] = 0
        self.config["success_count"] = 0
        self.config["fail_count"] = 0
        self.config["history"] = []
        self._save_config()
        print("统计数据已重置")

    def create_windows_task(self) -> bool:
        try:
            task_name = "NovelContentCollector"
            script_path = SCRIPTS_DIR / "auto_content_collector.py"
            python_path = PYTHON_EXECUTABLE

            day_map = {"周一": "MON", "周二": "TUE", "周三": "WED", "周四": "THU",
                       "周五": "FRI", "周六": "SAT", "周日": "SUN"}
            day = day_map.get(self.config["schedule"].get("day", "MON"), "MON")
            hour = self.config["schedule"].get("hour", 9)
            minute = self.config["schedule"].get("minute", 0)

            subprocess.run(f'schtasks /delete /tn "{task_name}" /f',
                           capture_output=True, shell=True)

            cmd = (f'schtasks /create /tn "{task_name}" '
                   f'/tr "\\"{python_path}\\" \\"{script_path}\\"" '
                   f'/sc weekly /d {day} /st {hour:02d}:{minute:02d}')

            result = subprocess.run(cmd, capture_output=True, shell=True)

            if result.returncode == 0:
                print(f"Windows计划任务已创建: {task_name}")
                print(f"  执行时间: {self._format_schedule_str()}")
                return True
            else:
                print(f"创建计划任务失败: {result.stderr.decode('utf-8', errors='ignore')}")
                return False

        except Exception as e:
            print(f"创建计划任务失败: {e}")
            return False


def main():
    if len(sys.argv) < 2:
        print("""
小说创作内容采集任务调度器 v3.0
============================================

用法: python task_scheduler.py [command] [options]

命令列表:
  status              显示任务状态
  run                 立即执行任务
  run -f              强制执行任务
  enable              启用任务
  disable             禁用任务
  history             显示执行历史
  history -n <num>    显示最近N条历史记录
  reset               重置统计数据

调度设置:
  update daily <hour> <minute>           更新为每天执行
  update weekly <day> <hour> <minute>    更新为每周执行
  update monthly <hour> <minute>         更新为每月执行

其他:
  windows-task        创建Windows计划任务
  check               检查是否到达执行时间并执行

示例:
  python task_scheduler.py status
  python task_scheduler.py run
  python task_scheduler.py update weekly 周三 10 30
  python task_scheduler.py history -n 20
""")
        return

    scheduler = TaskScheduler()
    command = sys.argv[1]

    if command == "status":
        scheduler.show_status()
    elif command == "run":
        force = len(sys.argv) > 2 and sys.argv[2] == "-f"
        scheduler.run_now(force=force)
    elif command == "enable":
        scheduler.enable()
    elif command == "disable":
        scheduler.disable()
    elif command == "history":
        limit = 10
        if len(sys.argv) > 2 and sys.argv[2] == "-n" and len(sys.argv) > 3:
            try:
                limit = int(sys.argv[3])
            except ValueError:
                print("参数错误: -n 需要一个数字")
                return
        scheduler.show_history(limit)
    elif command == "reset":
        scheduler.reset_stats()
    elif command == "update":
        if len(sys.argv) < 3:
            print("用法: update [daily|weekly|monthly] [day] [hour] [minute]")
            return
        schedule_type = sys.argv[2]
        day = sys.argv[3] if len(sys.argv) > 3 else None
        hour = int(sys.argv[4]) if len(sys.argv) > 4 else None
        minute = int(sys.argv[5]) if len(sys.argv) > 5 else None
        scheduler.update_schedule(schedule_type, day, hour, minute)
    elif command == "windows-task":
        scheduler.create_windows_task()
    elif command == "check":
        if scheduler.check_and_run():
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        print(f"未知命令: {command}")
        print("运行 'python task_scheduler.py' 查看帮助")


if __name__ == "__main__":
    main()
