"""
HarmonyOS NEXT UI/UX Pro Max Skill - Figma 资源抓取脚本
从 Figma 社区抓取 HarmonyOS NEXT 设计资源
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Optional

import requests
from colorama import init, Fore, Style

from config import (
    FIGMA_TOKEN, FIGMA_RESOURCES, FIGMA_OUTPUT_DIR,
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


class FigmaClient:
    """Figma API 客户端"""
    
    BASE_URL = "https://api.figma.com/v1"
    
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "X-Figma-Token": token,
            **DEFAULT_HEADERS
        }
    
    def get_file(self, file_key: str) -> Optional[Dict]:
        """
        获取 Figma 文件信息
        
        Args:
            file_key: 文件 Key
        
        Returns:
            文件信息
        """
        url = f"{self.BASE_URL}/files/{file_key}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            log_error(f"获取文件失败: {e}")
            return None
    
    def get_file_components(self, file_key: str) -> Optional[Dict]:
        """
        获取 Figma 文件中的组件
        
        Args:
            file_key: 文件 Key
        
        Returns:
            组件信息
        """
        url = f"{self.BASE_URL}/files/{file_key}/components"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            log_error(f"获取组件失败: {e}")
            return None
    
    def get_file_styles(self, file_key: str) -> Optional[Dict]:
        """
        获取 Figma 文件中的样式
        
        Args:
            file_key: 文件 Key
        
        Returns:
            样式信息
        """
        url = f"{self.BASE_URL}/files/{file_key}/styles"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            log_error(f"获取样式失败: {e}")
            return None
    
    def export_images(self, file_key: str, node_ids: List[str], format: str = "svg", scale: float = 1) -> Optional[Dict]:
        """
        导出节点为图片
        
        Args:
            file_key: 文件 Key
            node_ids: 节点 ID 列表
            format: 导出格式 (svg, png, jpg, pdf)
            scale: 缩放比例
        
        Returns:
            图片 URL 映射
        """
        url = f"{self.BASE_URL}/images/{file_key}"
        params = {
            "ids": ",".join(node_ids),
            "format": format,
            "scale": scale
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            log_error(f"导出图片失败: {e}")
            return None


def extract_file_key(url: str) -> Optional[str]:
    """
    从 Figma URL 提取文件 Key
    
    Args:
        url: Figma 文件 URL
    
    Returns:
        文件 Key
    """
    import re
    
    # 匹配 Figma 文件 URL 中的 Key
    # 格式: https://www.figma.com/file/FILE_KEY/...
    # 或: https://www.figma.com/community/file/FILE_KEY/...
    patterns = [
        r'figma\.com/file/([a-zA-Z0-9]+)',
        r'figma\.com/community/file/([a-zA-Z0-9]+)',
        r'figma\.com/design/([a-zA-Z0-9]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def extract_colors_from_styles(styles: Dict) -> List[Dict]:
    """
    从样式中提取颜色
    
    Args:
        styles: Figma 样式数据
    
    Returns:
        颜色列表
    """
    colors = []
    
    if not styles or "meta" not in styles:
        return colors
    
    for style in styles.get("meta", {}).get("styles", []):
        if style.get("style_type") == "FILL":
            colors.append({
                "name": style.get("name", ""),
                "description": style.get("description", ""),
                "key": style.get("key", "")
            })
    
    return colors


def extract_typography_from_styles(styles: Dict) -> List[Dict]:
    """
    从样式中提取字体样式
    
    Args:
        styles: Figma 样式数据
    
    Returns:
        字体样式列表
    """
    typography = []
    
    if not styles or "meta" not in styles:
        return typography
    
    for style in styles.get("meta", {}).get("styles", []):
        if style.get("style_type") == "TEXT":
            typography.append({
                "name": style.get("name", ""),
                "description": style.get("description", ""),
                "key": style.get("key", "")
            })
    
    return typography


def generate_design_tokens(file_data: Dict, styles: Dict, output_path: Path) -> None:
    """
    生成设计 Token 文件
    
    Args:
        file_data: Figma 文件数据
        styles: Figma 样式数据
        output_path: 输出路径
    """
    tokens = {
        "name": file_data.get("name", "HarmonyOS Design"),
        "lastModified": file_data.get("lastModified", ""),
        "colors": extract_colors_from_styles(styles),
        "typography": extract_typography_from_styles(styles),
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(tokens, f, indent=2, ensure_ascii=False)
    
    log_success(f"设计 Token 已生成: {output_path}")


def main():
    """主函数"""
    log_info("=" * 60)
    log_info("HarmonyOS NEXT UI/UX Pro Max Skill - Figma 资源抓取")
    log_info("=" * 60)
    
    # 检查 Figma Token
    if not FIGMA_TOKEN:
        log_warning("未设置 FIGMA_TOKEN 环境变量")
        log_info("请设置 FIGMA_TOKEN 环境变量后重试")
        log_info("获取 Token: https://www.figma.com/developers/api#access-tokens")
        
        # 生成示例设计 Token 文件
        log_info("\n生成示例设计 Token 文件...")
        ensure_dir(FIGMA_OUTPUT_DIR)
        
        sample_tokens = {
            "name": "HarmonyOS NEXT Design System",
            "description": "HarmonyOS NEXT 设计系统示例",
            "colors": {
                "primary": {
                    "main": "#0A59F7",
                    "light": "#5B8FF9",
                    "dark": "#0041C2"
                },
                "semantic": {
                    "success": "#64BB5C",
                    "warning": "#FA9D3B",
                    "error": "#E84026",
                    "info": "#0A59F7"
                },
                "neutral": {
                    "text_primary": "#182431",
                    "text_secondary": "#66727A",
                    "bg_primary": "#FFFFFF",
                    "bg_secondary": "#F1F3F5"
                }
            },
            "typography": {
                "font_family": "HarmonyOS Sans",
                "sizes": {
                    "xs": 10,
                    "sm": 12,
                    "md": 14,
                    "lg": 16,
                    "xl": 18,
                    "xxl": 20,
                    "display": 32
                },
                "weights": {
                    "regular": 400,
                    "medium": 500,
                    "bold": 700
                }
            },
            "spacing": {
                "xs": 4,
                "sm": 8,
                "md": 12,
                "lg": 16,
                "xl": 24,
                "xxl": 32
            },
            "border_radius": {
                "sm": 8,
                "md": 12,
                "lg": 16,
                "full": 9999
            }
        }
        
        sample_path = FIGMA_OUTPUT_DIR / "design_tokens_sample.json"
        with open(sample_path, 'w', encoding='utf-8') as f:
            json.dump(sample_tokens, f, indent=2, ensure_ascii=False)
        
        log_success(f"示例设计 Token 已生成: {sample_path}")
        return
    
    # 初始化 Figma 客户端
    client = FigmaClient(FIGMA_TOKEN)
    
    # 确保输出目录存在
    ensure_dir(FIGMA_OUTPUT_DIR)
    
    for resource_key, resource_info in FIGMA_RESOURCES.items():
        name = resource_info["name"]
        url = resource_info["url"]
        
        log_info(f"\n正在处理: {name}")
        
        # 提取文件 Key
        file_key = extract_file_key(url)
        if not file_key:
            log_error(f"无法从 URL 提取文件 Key: {url}")
            continue
        
        log_info(f"文件 Key: {file_key}")
        
        # 获取文件信息
        file_data = client.get_file(file_key)
        if not file_data:
            continue
        
        log_success(f"文件名: {file_data.get('name', 'Unknown')}")
        
        # 保存文件结构
        file_structure_path = FIGMA_OUTPUT_DIR / f"{resource_key}_structure.json"
        with open(file_structure_path, 'w', encoding='utf-8') as f:
            # 只保存基本结构，避免文件过大
            structure = {
                "name": file_data.get("name"),
                "lastModified": file_data.get("lastModified"),
                "version": file_data.get("version"),
                "document": {
                    "id": file_data.get("document", {}).get("id"),
                    "name": file_data.get("document", {}).get("name"),
                    "type": file_data.get("document", {}).get("type"),
                }
            }
            json.dump(structure, f, indent=2, ensure_ascii=False)
        
        log_success(f"文件结构已保存: {file_structure_path}")
        
        # 获取组件
        components = client.get_file_components(file_key)
        if components:
            components_path = FIGMA_OUTPUT_DIR / f"{resource_key}_components.json"
            with open(components_path, 'w', encoding='utf-8') as f:
                json.dump(components, f, indent=2, ensure_ascii=False)
            log_success(f"组件信息已保存: {components_path}")
        
        # 获取样式
        styles = client.get_file_styles(file_key)
        if styles:
            styles_path = FIGMA_OUTPUT_DIR / f"{resource_key}_styles.json"
            with open(styles_path, 'w', encoding='utf-8') as f:
                json.dump(styles, f, indent=2, ensure_ascii=False)
            log_success(f"样式信息已保存: {styles_path}")
            
            # 生成设计 Token
            tokens_path = FIGMA_OUTPUT_DIR / f"{resource_key}_tokens.json"
            generate_design_tokens(file_data, styles, tokens_path)
        
        time.sleep(REQUEST_DELAY)
    
    log_info("\n" + "=" * 60)
    log_success("Figma 资源抓取完成!")
    log_info("=" * 60)


if __name__ == "__main__":
    main()
