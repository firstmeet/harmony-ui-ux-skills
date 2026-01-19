"""
HarmonyOS NEXT UI/UX Pro Max Skill - 一键抓取所有资源
"""

import subprocess
import sys
from pathlib import Path

from colorama import init, Fore, Style

# 初始化 colorama
init()


def log_info(message: str):
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {message}")


def log_success(message: str):
    print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {message}")


def log_error(message: str):
    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {message}")


def run_script(script_name: str) -> bool:
    """
    运行 Python 脚本
    
    Args:
        script_name: 脚本名称
    
    Returns:
        是否运行成功
    """
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        log_error(f"脚本不存在: {script_path}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            cwd=script_path.parent
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        log_error(f"脚本执行失败: {e}")
        return False


def main():
    log_info("=" * 60)
    log_info("HarmonyOS NEXT UI/UX Pro Max Skill - 一键抓取所有资源")
    log_info("=" * 60)
    
    scripts = [
        ("fetch_figma_resources.py", "Figma 设计资源"),
        ("fetch_github_components.py", "GitHub/Gitee 组件"),
        ("fetch_ibest_ui.py", "IBest-UI 组件库"),
    ]
    
    results = []
    
    for script_name, description in scripts:
        log_info(f"\n{'=' * 40}")
        log_info(f"正在抓取: {description}")
        log_info(f"{'=' * 40}")
        
        success = run_script(script_name)
        results.append((description, success))
    
    # 打印总结
    log_info("\n" + "=" * 60)
    log_info("抓取结果总结:")
    log_info("=" * 60)
    
    for description, success in results:
        status = f"{Fore.GREEN}成功{Style.RESET_ALL}" if success else f"{Fore.RED}失败{Style.RESET_ALL}"
        log_info(f"  - {description}: {status}")
    
    success_count = sum(1 for _, s in results if s)
    log_info(f"\n总计: {success_count}/{len(results)} 成功")
    log_info("=" * 60)


if __name__ == "__main__":
    main()
