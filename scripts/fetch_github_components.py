"""
HarmonyOS NEXT UI/UX Pro Max Skill - GitHub/Gitee 组件抓取脚本
从 GitHub/Gitee 仓库抓取 ArkUI 组件和模板
"""

import os
import sys
import json
import time
import shutil
import zipfile
import tempfile
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urlparse

import requests
from tqdm import tqdm
from colorama import init, Fore, Style

from config import (
    GITHUB_REPOS, GITEE_REPOS, GITHUB_OUTPUT_DIR,
    REQUEST_TIMEOUT, MAX_RETRIES, REQUEST_DELAY,
    DEFAULT_HEADERS, SOURCE_FILE_EXTENSIONS, IGNORE_DIRS
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


def download_file(url: str, output_path: Path, headers: Dict = None) -> bool:
    """
    下载文件
    
    Args:
        url: 下载 URL
        output_path: 输出路径
        headers: 请求头
    
    Returns:
        是否下载成功
    """
    headers = headers or DEFAULT_HEADERS.copy()
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                url, 
                headers=headers, 
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


def download_github_repo(repo_info: Dict, output_dir: Path) -> bool:
    """
    下载 GitHub 仓库
    
    Args:
        repo_info: 仓库信息
        output_dir: 输出目录
    
    Returns:
        是否下载成功
    """
    name = repo_info["name"]
    url = repo_info["url"]
    branch = repo_info.get("branch", "main")
    
    log_info(f"正在下载仓库: {name}")
    
    # 解析 URL 获取仓库路径
    parsed = urlparse(url)
    path_parts = parsed.path.strip('/').split('/')
    
    if len(path_parts) < 2:
        log_error(f"无效的仓库 URL: {url}")
        return False
    
    owner, repo = path_parts[0], path_parts[1]
    
    # 构建下载 URL (ZIP 格式)
    if "github.com" in url:
        zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
    elif "gitee.com" in url:
        zip_url = f"https://gitee.com/{owner}/{repo}/repository/archive/{branch}.zip"
    else:
        log_error(f"不支持的仓库托管平台: {url}")
        return False
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        zip_path = temp_path / f"{name}.zip"
        
        # 下载 ZIP 文件
        if not download_file(zip_url, zip_path):
            log_error(f"下载仓库失败: {name}")
            return False
        
        # 解压 ZIP 文件
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_path)
            
            # 找到解压后的目录
            extracted_dirs = [d for d in temp_path.iterdir() if d.is_dir()]
            if not extracted_dirs:
                log_error(f"解压后未找到目录: {name}")
                return False
            
            extracted_dir = extracted_dirs[0]
            
            # 移动到输出目录
            repo_output_dir = output_dir / name
            if repo_output_dir.exists():
                shutil.rmtree(repo_output_dir)
            
            shutil.move(str(extracted_dir), str(repo_output_dir))
            
            log_success(f"仓库下载完成: {name}")
            return True
            
        except zipfile.BadZipFile as e:
            log_error(f"解压失败: {e}")
            return False


def extract_components(repo_dir: Path, output_dir: Path) -> List[Dict]:
    """
    从仓库中提取组件信息
    
    Args:
        repo_dir: 仓库目录
        output_dir: 输出目录
    
    Returns:
        提取的组件列表
    """
    components = []
    
    # 遍历所有源码文件
    for ext in SOURCE_FILE_EXTENSIONS:
        for file_path in repo_dir.rglob(f"*{ext}"):
            # 跳过忽略的目录
            if any(ignore_dir in str(file_path) for ignore_dir in IGNORE_DIRS):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查是否包含组件定义
                if '@Component' in content or 'struct' in content:
                    relative_path = file_path.relative_to(repo_dir)
                    
                    # 提取组件名称
                    component_names = extract_component_names(content)
                    
                    if component_names:
                        component_info = {
                            "file": str(relative_path),
                            "components": component_names,
                            "path": str(file_path)
                        }
                        components.append(component_info)
                        
            except Exception as e:
                log_warning(f"读取文件失败 {file_path}: {e}")
    
    return components


def extract_component_names(content: str) -> List[str]:
    """
    从代码内容中提取组件名称
    
    Args:
        content: 代码内容
    
    Returns:
        组件名称列表
    """
    import re
    
    names = []
    
    # 匹配 @Component struct ComponentName
    pattern = r'@Component\s+(?:export\s+)?struct\s+(\w+)'
    matches = re.findall(pattern, content)
    names.extend(matches)
    
    # 匹配 struct ComponentName
    pattern2 = r'(?:export\s+)?struct\s+(\w+)\s*\{'
    matches2 = re.findall(pattern2, content)
    for match in matches2:
        if match not in names:
            names.append(match)
    
    return names


def generate_component_index(components: List[Dict], output_path: Path) -> None:
    """
    生成组件索引文件
    
    Args:
        components: 组件列表
        output_path: 输出路径
    """
    index_data = {
        "total_files": len(components),
        "total_components": sum(len(c["components"]) for c in components),
        "components": components
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    log_success(f"组件索引已生成: {output_path}")


def main():
    """主函数"""
    log_info("=" * 60)
    log_info("HarmonyOS NEXT UI/UX Pro Max Skill - GitHub 组件抓取")
    log_info("=" * 60)
    
    # 确保输出目录存在
    ensure_dir(GITHUB_OUTPUT_DIR)
    
    all_components = []
    
    # 下载 GitHub 仓库
    log_info("\n正在下载 GitHub 仓库...")
    for repo_info in GITHUB_REPOS:
        if download_github_repo(repo_info, GITHUB_OUTPUT_DIR):
            repo_dir = GITHUB_OUTPUT_DIR / repo_info["name"]
            components = extract_components(repo_dir, GITHUB_OUTPUT_DIR)
            
            log_info(f"从 {repo_info['name']} 提取了 {len(components)} 个组件文件")
            
            for comp in components:
                comp["source"] = repo_info["name"]
            all_components.extend(components)
        
        time.sleep(REQUEST_DELAY)
    
    # 下载 Gitee 仓库
    log_info("\n正在下载 Gitee 仓库...")
    for repo_info in GITEE_REPOS:
        if download_github_repo(repo_info, GITHUB_OUTPUT_DIR):
            repo_dir = GITHUB_OUTPUT_DIR / repo_info["name"]
            components = extract_components(repo_dir, GITHUB_OUTPUT_DIR)
            
            log_info(f"从 {repo_info['name']} 提取了 {len(components)} 个组件文件")
            
            for comp in components:
                comp["source"] = repo_info["name"]
            all_components.extend(components)
        
        time.sleep(REQUEST_DELAY)
    
    # 生成组件索引
    if all_components:
        index_path = GITHUB_OUTPUT_DIR / "component_index.json"
        generate_component_index(all_components, index_path)
    
    log_info("\n" + "=" * 60)
    log_success(f"抓取完成! 共提取 {len(all_components)} 个组件文件")
    log_info("=" * 60)


if __name__ == "__main__":
    main()
