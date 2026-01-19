"""
HarmonyOS NEXT UI/UX Pro Max Skill - IBest-UI 组件库抓取脚本
从 NPM/OHPM 抓取 IBest-UI 组件库并分析其结构
"""

import os
import sys
import json
import time
import tarfile
import tempfile
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple

import requests
from tqdm import tqdm
from colorama import init, Fore, Style

from config import (
    NPM_PACKAGES, COMPONENTS_OUTPUT_DIR,
    REQUEST_TIMEOUT, MAX_RETRIES, REQUEST_DELAY,
    DEFAULT_HEADERS
)

# 初始化 colorama
init()


def log_info(message: str):
    """打印信息日志"""
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {message}")


def log_success(message: str):
    """打印成功日志"""
    print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {message}")


def log_warning(message: str):
    """打印警告日志"""
    print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {message}")


def log_error(message: str):
    """打印错误日志"""
    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {message}")


def ensure_dir(path: Path) -> None:
    """确保目录存在"""
    path.mkdir(parents=True, exist_ok=True)


def fetch_npm_package_info(package_name: str, registry: str) -> Optional[Dict]:
    """
    获取 NPM 包信息
    
    Args:
        package_name: 包名
        registry: 注册表 URL
    
    Returns:
        包信息字典
    """
    url = f"{registry}/{package_name}/latest"
    
    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        log_error(f"获取包信息失败: {e}")
        return None


def download_npm_package(tarball_url: str, output_path: Path) -> bool:
    """
    下载 NPM 包 tarball
    
    Args:
        tarball_url: tarball 下载 URL
        output_path: 输出路径
    
    Returns:
        是否下载成功
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                tarball_url,
                headers=DEFAULT_HEADERS,
                timeout=REQUEST_TIMEOUT,
                stream=True
            )
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(output_path, 'wb') as f:
                if total_size > 0:
                    with tqdm(total=total_size, unit='B', unit_scale=True, desc=output_path.name) as pbar:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))
                else:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            
            return True
            
        except requests.exceptions.RequestException as e:
            log_warning(f"下载失败 (尝试 {attempt + 1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(REQUEST_DELAY)
    
    return False


def extract_tarball(tarball_path: Path, output_dir: Path) -> bool:
    """
    解压 tarball 文件
    
    Args:
        tarball_path: tarball 文件路径
        output_dir: 输出目录
    
    Returns:
        是否解压成功
    """
    try:
        with tarfile.open(tarball_path, 'r:gz') as tar:
            tar.extractall(output_dir)
        return True
    except Exception as e:
        log_error(f"解压失败: {e}")
        return False


def analyze_component_structure(package_dir: Path) -> Dict:
    """
    分析组件库结构
    
    Args:
        package_dir: 包目录
    
    Returns:
        组件结构分析结果
    """
    analysis = {
        "components": [],
        "themes": [],
        "styles": [],
        "utils": [],
        "types": []
    }
    
    # 遍历目录结构
    for item in package_dir.rglob("*"):
        if item.is_file():
            relative_path = str(item.relative_to(package_dir))
            
            if item.suffix in ['.ets', '.ts']:
                content = ""
                try:
                    with open(item, 'r', encoding='utf-8') as f:
                        content = f.read()
                except:
                    pass
                
                # 分析组件
                if '@Component' in content or 'struct' in content:
                    component_info = extract_component_info(content, relative_path)
                    if component_info:
                        analysis["components"].append(component_info)
                
                # 分析主题
                if 'theme' in relative_path.lower() or 'color' in relative_path.lower():
                    analysis["themes"].append(relative_path)
                
                # 分析样式
                if 'style' in relative_path.lower():
                    analysis["styles"].append(relative_path)
                
                # 分析工具函数
                if 'util' in relative_path.lower() or 'helper' in relative_path.lower():
                    analysis["utils"].append(relative_path)
                
                # 分析类型定义
                if 'type' in relative_path.lower() or 'interface' in content:
                    analysis["types"].append(relative_path)
    
    return analysis


def extract_component_info(content: str, file_path: str) -> Optional[Dict]:
    """
    从代码中提取组件信息
    
    Args:
        content: 代码内容
        file_path: 文件路径
    
    Returns:
        组件信息
    """
    # 匹配组件名称
    struct_match = re.search(r'@Component\s+(?:export\s+)?struct\s+(\w+)', content)
    if not struct_match:
        struct_match = re.search(r'(?:export\s+)?struct\s+(\w+)\s*\{', content)
    
    if not struct_match:
        return None
    
    component_name = struct_match.group(1)
    
    # 提取 Props
    props = extract_props(content)
    
    # 提取 State
    states = extract_states(content)
    
    return {
        "name": component_name,
        "file": file_path,
        "props": props,
        "states": states
    }


def extract_props(content: str) -> List[Dict]:
    """
    提取组件 Props
    
    Args:
        content: 代码内容
    
    Returns:
        Props 列表
    """
    props = []
    
    # 匹配 @Prop 装饰器
    prop_pattern = r'@Prop\s+(?:@\w+\s+)*(\w+)\s*:\s*(\w+(?:<[^>]+>)?)'
    matches = re.findall(prop_pattern, content)
    
    for name, type_str in matches:
        props.append({
            "name": name,
            "type": type_str,
            "decorator": "@Prop"
        })
    
    return props


def extract_states(content: str) -> List[Dict]:
    """
    提取组件 State
    
    Args:
        content: 代码内容
    
    Returns:
        State 列表
    """
    states = []
    
    # 匹配 @State 装饰器
    state_pattern = r'@State\s+(?:@\w+\s+)*(\w+)\s*:\s*(\w+(?:<[^>]+>)?)'
    matches = re.findall(state_pattern, content)
    
    for name, type_str in matches:
        states.append({
            "name": name,
            "type": type_str,
            "decorator": "@State"
        })
    
    return states


def generate_analysis_report(analysis: Dict, output_path: Path) -> None:
    """
    生成分析报告
    
    Args:
        analysis: 分析结果
        output_path: 输出路径
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    log_success(f"分析报告已生成: {output_path}")


def main():
    """主函数"""
    log_info("=" * 60)
    log_info("HarmonyOS NEXT UI/UX Pro Max Skill - IBest-UI 抓取")
    log_info("=" * 60)
    
    # 确保输出目录存在
    ensure_dir(COMPONENTS_OUTPUT_DIR)
    
    for package_info in NPM_PACKAGES:
        package_name = package_info["name"]
        registry = package_info["registry"]
        
        log_info(f"\n正在处理包: {package_name}")
        
        # 获取包信息
        npm_info = fetch_npm_package_info(package_name, registry)
        if not npm_info:
            continue
        
        version = npm_info.get("version", "unknown")
        tarball_url = npm_info.get("dist", {}).get("tarball")
        
        log_info(f"版本: {version}")
        
        if not tarball_url:
            log_error("未找到 tarball URL")
            continue
        
        # 下载包
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            tarball_path = temp_path / f"{package_name.replace('/', '_')}.tgz"
            
            log_info(f"正在下载: {tarball_url}")
            if not download_npm_package(tarball_url, tarball_path):
                continue
            
            # 解压包
            log_info("正在解压...")
            if not extract_tarball(tarball_path, temp_path):
                continue
            
            # 找到解压后的目录 (通常是 'package')
            package_dir = temp_path / "package"
            if not package_dir.exists():
                # 尝试找到其他目录
                dirs = [d for d in temp_path.iterdir() if d.is_dir()]
                if dirs:
                    package_dir = dirs[0]
                else:
                    log_error("未找到解压后的目录")
                    continue
            
            # 分析组件结构
            log_info("正在分析组件结构...")
            analysis = analyze_component_structure(package_dir)
            
            # 复制到输出目录
            output_package_dir = COMPONENTS_OUTPUT_DIR / package_name.replace('/', '_').replace('@', '')
            if output_package_dir.exists():
                import shutil
                shutil.rmtree(output_package_dir)
            
            import shutil
            shutil.copytree(package_dir, output_package_dir)
            
            # 生成分析报告
            report_path = output_package_dir / "analysis_report.json"
            generate_analysis_report(analysis, report_path)
            
            log_success(f"包处理完成: {package_name}")
            log_info(f"  - 组件数: {len(analysis['components'])}")
            log_info(f"  - 主题文件: {len(analysis['themes'])}")
            log_info(f"  - 样式文件: {len(analysis['styles'])}")
        
        time.sleep(REQUEST_DELAY)
    
    log_info("\n" + "=" * 60)
    log_success("IBest-UI 抓取完成!")
    log_info("=" * 60)


if __name__ == "__main__":
    main()
